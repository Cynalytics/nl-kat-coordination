from collections.abc import Iterable
from datetime import datetime
from typing import Any

from django.utils.translation import gettext_lazy as _

from octopoes.models.ooi.network import IPAddressV4, IPAddressV6
from reports.report_types.definitions import Report


class CynalyticsReport(Report):
    id = "cynalytics-report"
    name = _("Cynalytics report")
    description = _("Find open ports of IP addresses")
    input_ooi_types = {IPAddressV4, IPAddressV6}
    template_path = "cynalytics_report/report.html"
    label_style = "5-light"

    def collect_data(self, input_oois: Iterable[str], valid_time: datetime) -> dict[str, dict[Any, Any]]:
        ips_by_input_ooi = self.to_ips(input_oois, valid_time)
        all_ips = list({ip for key, ips in ips_by_input_ooi.items() for ip in ips})
        ports_by_source = self.group_by_source(
            self.octopoes_api_connector.query_many("IPAddress.<address[is IPPort]", valid_time, all_ips)
        )
        all_ports = [port for key, ports in ports_by_source.items() for port in ports]

        hostnames_by_source = self.group_by_source(
            self.octopoes_api_connector.query_many(
                "IPAddress.<address[is ResolvedHostname].hostname", valid_time, all_ips
            )
        )
        services_by_port = self.group_by_source(
            self.octopoes_api_connector.query_many("IPPort.<ip_port[is IPService].service", valid_time, all_ports)
        )
        result = {"abc": ips_by_input_ooi, "abc3": hostnames_by_source, "abc4": services_by_port}
        return result
