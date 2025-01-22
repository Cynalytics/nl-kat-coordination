import json
from collections.abc import Iterable
from datetime import datetime
from typing import Any

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
        result: dict[str, list] = {
            "common_ports": [67, 68, 80, 162, 427, 443, 993, 995],
            "critical_ports": [20, 21, 23, 69, 110, 137, 138, 139, 143, 161, 389, 445, 3389],
            "dangerous_ports": [22, 25, 53],
            "scanned_ips": [],
        }
        for input_ooi, ips in open_ports_result.items():
            for ip, data in ips.items():
                ip_scan = {"input_ooi": input_ooi, "ip": ip, "open_ports": []}
                for port in data["services"]:
                    ip_scan["open_ports"].append(port)

                result["scanned_ips"].append(ip_scan)
        result["chart"] = [
            {"label": "apple", "y": 10},
            {"label": "orange", "y": 15},
            {"label": "banana", "y": 25},
            {"label": "mango", "y": 30},
            {"label": "grape", "y": 28},
        ]
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
