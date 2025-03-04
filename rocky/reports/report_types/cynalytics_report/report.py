from datetime import datetime
from typing import Any

import structlog
from django.utils.translation import gettext_lazy as _

from octopoes.models import Reference
from octopoes.models.ooi.dns.zone import ResolvedHostname
from octopoes.models.ooi.network import IPAddress
from octopoes.models.ooi.web import Hostname, Website
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
        related_ips = self.octopoes_api_connector.get_tree(hostname_ref, valid_time, depth=1, types={IPAddress}).store
        related_resolved_hostnames = self.octopoes_api_connector.get_tree(
            hostname_ref, valid_time, depth=1, types={ResolvedHostname}
        ).store

        data: dict[str, Any] = {"ipv4_reachable": False, "ipv6_reachable": False}

        for related_website in related_websites.values():
            if related_website.ip_service.ip_address.object_type == "IPAddressV4":
                data["ipv4_reachable"] = True
            elif related_website.ip_service.ip_address.object_type == "IPAddressV6":
                data["ipv6_reachable"] = True
        data["ipv4_reachable"] = True

        return related_websites | related_ips | related_resolved_hostnames | {"a": b"c"}
