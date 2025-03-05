from datetime import datetime
from typing import Any

import structlog
from django.utils.translation import gettext_lazy as _

from octopoes.models import Reference
from octopoes.models.ooi.dns.zone import ResolvedHostname
from octopoes.models.ooi.network import IPAddress
from octopoes.models.ooi.web import Hostname, Website
from octopoes.models.types import OOIType
from reports.report_types.definitions import Report

logger = structlog.get_logger(__name__)


class CynalyticsReport(Report):
    id = "cynalytics-report"
    name = _("Cynalytics report")
    description = _("A Cynalytics report.")
    plugins = {"required": set(), "optional": set()}
    input_ooi_types = {Hostname}
    template_path = "cynalytics_report/report.html"
    label_style = "5-light"

    def generate_data(self, input_ooi: str, valid_time: datetime) -> dict[str, Any]:
        hostname_ref = Reference.from_str(input_ooi)
        related_websites = self.octopoes_api_connector.get_tree(
            hostname_ref, valid_time, depth=1, types={Website}
        ).store
        related_resolved_hostnames = self.octopoes_api_connector.get_tree(
            hostname_ref, valid_time, depth=1, types={ResolvedHostname}
        ).store

        related_ips: dict[str, OOIType] = {}
        for related_resolved_hostname in related_resolved_hostnames:
            related_ips.update(
                self.octopoes_api_connector.get_tree(
                    Reference.from_str(related_resolved_hostname), valid_time, depth=1, types={IPAddress}
                ).store
            )

        data: dict[str, Any] = {
            "ipv4_reachable": False,
            "ipv6_reachable": False,
            "debug": related_websites | related_ips | related_resolved_hostnames,
        }

        for related_ip in related_ips.values():
            if related_ip.object_type == "IPAddressV4":
                data["ipv4_reachable"] = True
            elif related_ip.object_type == "IPAddressV6":
                data["ipv6_reachable"] = True

        return data
