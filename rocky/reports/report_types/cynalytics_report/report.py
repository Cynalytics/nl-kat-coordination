from datetime import datetime
from typing import Any, Literal

import structlog
from django.utils.translation import gettext_lazy as _

from octopoes.models import Reference
from octopoes.models.ooi.dns.zone import Hostname, ResolvedHostname
from octopoes.models.ooi.network import IPAddress
from octopoes.models.ooi.web import Website
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

        findings = self.octopoes_api_connector.list_findings([], valid_time, search_string=hostname_ref).items

        tasks = self.scheduler_client.completed_tasks_by_ooi(hostname_ref)

        # dns_sec can be "unknown"
        dns_sec: Literal["unknown", "bad", "good"] = "unknown"
        if any([x.finding_type == "KATFindingType|KAT-NO-DNSSEC" for x in findings]):
            dns_sec = "bad"
        elif "dns-sec" in tasks:
            # if dns-sec has been ran and no finding is found, it is good
            dns_sec = "good"

        data: dict[str, Any] = {
            "ipv4_reachable": False,
            "ipv6_reachable": False,
            "fulfilled_tasks": tasks,
            "dns_sec": dns_sec,
            "findings": [x.model_dump() for x in findings],
            "debug": related_websites | related_ips | related_resolved_hostnames,
        }

        for related_ip in related_ips.values():
            if related_ip.object_type == "IPAddressV4":
                data["ipv4_reachable"] = True
            elif related_ip.object_type == "IPAddressV6":
                data["ipv6_reachable"] = True

        return data
