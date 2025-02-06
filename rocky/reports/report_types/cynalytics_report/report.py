import base64
import json
from collections.abc import Iterable
from datetime import datetime
from io import BytesIO
from typing import Any

import matplotlib.pyplot as plt
import structlog
from django.utils.translation import gettext_lazy as _

from octopoes.models.ooi.network import IPAddressV4, IPAddressV6
from reports.report_types.definitions import Report

logger = structlog.get_logger(__name__)


class CynalyticsReport(Report):
    id = "cynalytics-report"
    name = _("Cynalytics report")
    description = _("Find open ports of IP addresses")
    plugins = {"required": {"nmap"}, "optional": set()}
    input_ooi_types = {IPAddressV4, IPAddressV6}
    template_path = "cynalytics_report/report.html"
    label_style = "5-light"

    def collect_data(self, input_oois: Iterable[str], valid_time: datetime) -> dict[str, Any]:
        open_ports_result = self.open_ports_report(input_oois, valid_time)

        # SOURCE: https://support.huawei.com/enterprise/en/doc/EDOC1100297670
        COMMON_PORTS = [67, 68, 80, 162, 427, 443, 993, 995]
        DANGEROUS_PORTS = [22, 25, 53]
        CRITICAL_PORTS = [20, 21, 23, 69, 110, 137, 138, 139, 143, 161, 389, 445, 3389]

        result: dict[str, dict[str, Any]] = {}
        for input_ooi, ips in open_ports_result.items():
            for ip, data in ips.items():
                result[input_ooi] = {
                    "open_ports": [],
                    "ip": ip,
                    "chart": [
                        {"label": "common", "count": 0},
                        {"label": "dangerous", "count": 0},
                        {"label": "critical", "count": 0},
                        {"label": "unknown", "count": 0},
                    ],
                }
                open_ports: list[tuple[str, int]] = []
                for port in data["services"]:
                    if port in COMMON_PORTS:
                        open_ports.append(("common", port))
                        result[input_ooi]["chart"][0]["count"] += 1
                    elif port in DANGEROUS_PORTS:
                        open_ports.append(("dangerous", port))
                        result[input_ooi]["chart"][1]["count"] += 1
                    elif port in CRITICAL_PORTS:
                        open_ports.append(("critical", port))
                        result[input_ooi]["chart"][2]["count"] += 1
                    else:
                        open_ports.append(("unknown", port))
                        result[input_ooi]["chart"][3]["count"] += 1
                result[input_ooi]["open_ports"] = sorted(open_ports, key=lambda d: d[1])

                #! NEW GRAPH
                labels = "Frogs", "Hogs", "Dogs", "Logs"
                sizes = [15, 30, 45, 10]

                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, colors=["red", "blue", "green", "yellow"])

                buffer = BytesIO()
                plt.savefig(buffer, format="png")
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()

                graphic = base64.b64encode(image_png).decode("utf-8")
                result[input_ooi]["chart_image"] = graphic

                # // with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                # //     plt.savefig(tmpfile.name, dpi=500)
                # //     result[input_ooi]["chart_image"] = tmpfile.name

                #!
        logger.info("Cynalytics report collected data", result=json.dumps(result))
        return result

    def open_ports_report(self, input_oois: Iterable[str], valid_time: datetime):
        ips_by_input_ooi = self.to_ips(input_oois, valid_time)
        all_ips = list({ip for _, ips in ips_by_input_ooi.items() for ip in ips})
        ports_by_source = self.group_by_source(
            self.octopoes_api_connector.query_many("IPAddress.<address[is IPPort]", valid_time, all_ips)
        )
        all_ports = [port for _, ports in ports_by_source.items() for port in ports]

        hostnames_by_source = self.group_by_source(
            self.octopoes_api_connector.query_many(
                "IPAddress.<address[is ResolvedHostname].hostname", valid_time, all_ips
            )
        )
        services_by_port = self.group_by_source(
            self.octopoes_api_connector.query_many("IPPort.<ip_port[is IPService].service", valid_time, all_ports)
        )
        result = {}

        for input_ooi, ips in ips_by_input_ooi.items():
            by_ip = {}

            for ip in ips:
                ports = ports_by_source.get(ip, [])
                hostnames = [h.name for h in hostnames_by_source.get(ip, [])]

                port_numbers = {}
                services = {}

                for port in ports:
                    origins = self.octopoes_api_connector.list_origins(result=port.reference, valid_time=valid_time)
                    found_by_openkat = any(o.method in ("kat_nmap_normalize", "kat_masscan_normalize") for o in origins)
                    port_numbers[port.port] = found_by_openkat
                    services[port.port] = [service.name for service in services_by_port.get(port.reference, [])]

                sorted_port_numbers = dict(sorted(port_numbers.items()))
                by_ip[ip.tokenized.address] = {
                    "ports": sorted_port_numbers,
                    "hostnames": hostnames,
                    "services": services,
                }

            result[input_ooi] = by_ip

        return result
