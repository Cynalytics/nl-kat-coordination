from collections.abc import Iterable
from datetime import datetime
from logging import getLogger
from typing import Any

from django.utils.translation import gettext_lazy as _

from octopoes.models.ooi.greeting import Greeting
from octopoes.models.ooi.network import IPAddressV4, IPAddressV6
from reports.report_types.definitions import Report

logger = getLogger(__name__)


class GreetingsReport(Report):
    id = "greetings-report"
    name = _("Greetings report")
    description = _("Sends a greeting to the user")
    plugins = {"required": ["nmap"], "optional": ["shodan", "nmap-udp", "nmap-ports", "nmap-ip-range", "masscan"]}
    input_ooi_types = {Greeting, IPAddressV4, IPAddressV6} # consumes
    template_path = "greetings_report/report.html"

    def generate_data(self, input_ooi: str, valid_time: datetime) -> dict[str, Any]:
        return {"greeting": "Hello Katty!", "input_ooi": input_ooi}
