from typing import Any, Dict

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django_weasyprint import WeasyTemplateResponseMixin
from tools.view_helpers import url_with_querystring

from octopoes.models import Reference
from reports.report_types.multi_organization_report.report import MultiOrganizationReport
from reports.views.base import (
    BaseReportView,
    ReportBreadcrumbs,
)
from rocky.views.ooi_view import BaseOOIListView


class BreadcrumbsMultiReportView(ReportBreadcrumbs):
    def build_breadcrumbs(self):
        breadcrumbs = super().build_breadcrumbs()
        kwargs = self.get_kwargs()
        selection = self.get_selection()
        breadcrumbs += [
            {
                "url": reverse("multi_report_landing", kwargs=kwargs) + selection,
                "text": _("Multi report"),
            },
            {
                "url": reverse("multi_report_select_oois", kwargs=kwargs) + selection,
                "text": _("Select OOIs"),
            },
            {
                "url": reverse("multi_report_select_report_types", kwargs=kwargs) + selection,
                "text": _("Select report types"),
            },
            {
                "url": reverse("multi_report_setup_scan", kwargs=kwargs) + selection,
                "text": _("Setup scan"),
            },
            {
                "url": reverse("multi_report_view", kwargs=kwargs) + selection,
                "text": _("View report"),
            },
        ]
        return breadcrumbs


class LandingMultiReportView(BreadcrumbsMultiReportView, TemplateView):
    """
    Landing page to start the 'Multi Report' flow.
    """

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return redirect(reverse("multi_report_select_oois", kwargs=self.get_kwargs()) + self.get_selection())


class OOISelectionMultiReportView(BreadcrumbsMultiReportView, BaseReportView, BaseOOIListView):
    """
    Select OOIs for the 'Multi Report' flow.
    """

    template_name = "generate_report/select_oois.html"
    current_step = 3
    ooi_types = MultiOrganizationReport.input_ooi_types

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_ooi_filter_forms(self.ooi_types))
        return context


class ReportTypesSelectionMultiReportView(BreadcrumbsMultiReportView, BaseReportView, TemplateView):
    """
    Shows all possible report types from a list of OOIs.
    Chooses report types for the 'Multi Report' flow.
    """

    template_name = "generate_report/select_report_types.html"
    current_step = 4

    def get(self, request, *args, **kwargs):
        if not self.selected_oois:
            messages.error(self.request, _("Select at least one OOI to proceed."))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["oois"] = self.get_oois()
        context["available_report_types"] = self.get_report_types_for_generate_report([MultiOrganizationReport])
        return context


class SetupScanMultiReportView(BreadcrumbsMultiReportView, BaseReportView, TemplateView):
    """
    Show required and optional plugins to start scans to multi OOIs to include in report.
    """

    template_name = "generate_report/setup_scan.html"
    current_step = 5

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not self.selected_report_types:
            messages.error(self.request, _("Select at least one report type to proceed."))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plugins"] = {"required": [], "optional": []}
        return context


class MultiReportView(BreadcrumbsMultiReportView, BaseReportView, TemplateView):
    """
    Shows the report multid from OOIS and report types.
    """

    template_name = "multi_report.html"
    current_step = 6

    def multi_reports_for_oois(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        report_data = {}
        for ooi in self.selected_oois:
            report_data[ooi] = {}
            for report_type in [MultiOrganizationReport]:
                if Reference.from_str(ooi).class_type in report_type.input_ooi_types:
                    report = report_type(self.octopoes_api_connector)
                    data = report.generate_data(ooi, valid_time=self.valid_time)
                    template = report.template_path
                    report_data[ooi][report_type.name] = {"data": data, "template": template}
        return report_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["oois"] = self.get_oois()
        context["report_types"] = [MultiOrganizationReport]
        context["report_data"] = self.multi_reports_for_oois()
        context["report_download_url"] = url_with_querystring(
            reverse("multi_report_pdf", kwargs={"organization_code": self.organization.code}),
            True,
            **self.request.GET,
        )
        return context


class MultiReportPDFView(MultiReportView, WeasyTemplateResponseMixin):
    template_name = "multi_report_pdf.html"

    pdf_filename = "multi_report.pdf"
    pdf_attachment = False
    pdf_options = {
        "pdf_variant": "pdf/ua-1",
    }