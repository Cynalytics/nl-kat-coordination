from datetime import datetime
from logging import getLogger
from typing import Any, Dict, List

from django.utils.translation import gettext_lazy as _

from octopoes.models import Reference
from octopoes.models.ooi.dns.zone import Hostname
from octopoes.models.ooi.network import IPAddressV4, IPAddressV6
from reports.report_types.definitions import Report

logger = getLogger(__name__)

MAIL_FINDINGS = ["KAT-NO-SPF", "KAT-NO-DMARC", "KAT-NO-DKIM"]


class MailReport(Report):
    id = "mail-report"
    name = _("Mail Report")
    description = _("System specific mail report that focusses on IP addresses and hostnames.")
    plugins = {"required": ["dns-records"], "optional": []}
    input_ooi_types = {Hostname, IPAddressV4, IPAddressV6}
    template_path = "mail_report/report.html"

    def generate_data(self, input_ooi: str, valid_time: datetime) -> Dict[str, Any]:
        reference = Reference.from_str(input_ooi)
        hostnames = []
        mail_security_measures = {}

        if reference.class_type == Hostname:
            hostnames = [reference]
        elif reference.class_type in (IPAddressV4, IPAddressV6):
            hostnames = self.octopoes_api_connector.query(
                "IPAddress.<address[is ResolvedHostname].hostname", valid_time, reference
            )

        number_of_hostnames = len(hostnames)
        number_of_spf = number_of_hostnames
        number_of_dmarc = number_of_hostnames
        number_of_dkim = number_of_hostnames

        for hostname in hostnames:
            measures = self._get_measures(valid_time, hostname)

            if reference.class_type == Hostname:
                mail_security_measures = {"hostname": hostnames[0].tokenized.name, "measures": measures}
            else:
                mail_security_measures.update({"hostname": hostname.name, "measures": measures})

            number_of_spf -= (
                1 if list(filter(lambda finding: finding.id == "KAT-NO-SPF", mail_security_measures["measures"])) else 0
            )
            number_of_dmarc -= (
                1
                if list(filter(lambda finding: finding.id == "KAT-NO-DMARC", mail_security_measures["measures"]))
                else 0
            )
            number_of_dkim -= (
                1
                if list(filter(lambda finding: finding.id == "KAT-NO-DKIM", mail_security_measures["measures"]))
                else 0
            )

        return {
            "input_ooi": input_ooi,
            "mail_security_measures": mail_security_measures,
            "number_of_hostnames": number_of_hostnames,
            "number_of_spf": number_of_spf,
            "number_of_dmarc": number_of_dmarc,
            "number_of_dkim": number_of_dkim,
        }

    def _get_measures(self, valid_time: datetime, hostname) -> List[Dict[str, Any]]:
        finding_types = []
        measures = []
        finding_types = self.octopoes_api_connector.query(
            "Hostname.<ooi[is Finding].finding_type", valid_time, hostname
        )

        measures = list(filter(lambda finding: finding.id in MAIL_FINDINGS, finding_types))
        return measures