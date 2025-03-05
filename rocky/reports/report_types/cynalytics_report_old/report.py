import base64
import json
from collections.abc import Iterable
from datetime import datetime
from io import BytesIO
from typing import Any

import matplotlib.pyplot as plt
import structlog
from django.utils.translation import gettext_lazy as _

from octopoes.models import Reference
from octopoes.models.ooi.network import IPAddressV4, IPAddressV6
from reports.report_types.definitions import Report

logger = structlog.get_logger(__name__)


class CynalyticsOldReport(Report):
    id = "cynalytics-report-old"
    name = _("Cynalytics report old")
    description = _("An old Cynalytics report.")
    plugins = {"required": {"nmap"}, "optional": set()}
    input_ooi_types = {IPAddressV4, IPAddressV6}
    template_path = "cynalytics_report_old/report.html"
    label_style = "5-light"

    def collect_data(self, input_oois: Iterable[str], valid_time: datetime) -> dict[Reference, dict[str, Any]]:
        open_ports_result = self.open_ports_report(input_oois, valid_time)

        # SOURCE: https://support.huawei.com/enterprise/en/doc/EDOC1100297670
        COMMON_PORTS = {67, 68, 80, 162, 427, 443, 993, 995}
        DANGEROUS_PORTS = {22, 25, 53}
        CRITICAL_PORTS = {20, 21, 23, 69, 110, 137, 138, 139, 143, 161, 389, 445, 3389}

        result: dict[Reference, dict[str, Any]] = {}
        for input_ooi, ips in open_ports_result.items():
            for __, data in ips.items():
                common_open_ports: set[int] = set()
                dangerous_open_ports: set[int] = set()
                critical_open_ports: set[int] = set()
                unknown_open_ports: set[int] = set()

                for port in data["services"]:
                    if port in COMMON_PORTS:
                        common_open_ports.add(port)
                    elif port in DANGEROUS_PORTS:
                        dangerous_open_ports.add(port)
                    elif port in CRITICAL_PORTS:
                        critical_open_ports.add(port)
                    else:
                        unknown_open_ports.add(port)

                #! NEW GRAPH

                labels: list[str] = []
                sizes: list[int] = []
                colors: list[str] = []

                port_categories = [
                    ("Common port", common_open_ports, "blue"),
                    ("Dangerous port", dangerous_open_ports, "orange"),
                    ("Critical port", critical_open_ports, "red"),
                    ("Unknown port", unknown_open_ports, "gray"),
                ]

                for label, ports, color in port_categories:
                    if len(ports) > 0:
                        labels.append(label)
                        sizes.append(len(ports))
                        colors.append(color)

                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, colors=colors)

                buffer = BytesIO()
                plt.savefig(buffer, format="png")
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()

                result[input_ooi] = {
                    "open_ports": {
                        "common": sorted(common_open_ports),
                        "dangerous": sorted(dangerous_open_ports),
                        "critical": sorted(critical_open_ports),
                        "unknown": sorted(unknown_open_ports),
                    },
                    "chart_image": base64.b64encode(image_png).decode("utf-8"),
                }

                #!
        logger.info("Cynalytics report collected data", result=json.dumps(result))
        return result

    def open_ports_report(self, input_oois: Iterable[str], valid_time: datetime) -> dict[Reference, dict[str, Any]]:
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
