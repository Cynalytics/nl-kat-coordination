from typing import Any

import httpx
import structlog
from django.conf import settings

from octopoes.models import Reference
from rocky.health import ServiceHealth

logger = structlog.get_logger(__name__)


class SchedulerClient:
    def __init__(self, organization: str | None):
        self.session = httpx.Client(base_url=settings.SCHEDULER_API, timeout=settings.ROCKY_OUTGOING_REQUEST_TIMEOUT)
        self.organization = organization

    def health(self) -> ServiceHealth:
        response = self.session.get("/health")
        response.raise_for_status()

        return ServiceHealth.model_validate(response.json())

    def completed_tasks_by_ooi(self, ooi: Reference) -> list[str]:
        response = self.session.get(
            "/tasks",
            params={
                "scheduler_id": f"boefje-{self.organization}",
                "task_type": "boefje",
                "status": "completed",
                "input_ooi": str(ooi),
            },
        )

        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return list({x["data"]["boefje"]["id"] for x in data["results"]})
