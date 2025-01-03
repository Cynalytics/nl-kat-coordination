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
    plugins = {"required": set(), "optional": set()}
    input_ooi_types = {IPAddressV4, IPAddressV6}
    template_path = "cynalytics_report/report.html"
    label_style = "5-light"

    def collect_data(self, input_oois: Iterable[str], valid_time: datetime) -> dict[str, dict[Any, Any]]:
        return {"abc": {"abc2": "abc"}}
