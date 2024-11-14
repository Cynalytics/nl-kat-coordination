from collections.abc import Set
from typing import Any

import fastapi
import structlog
from fastapi import status
from pydantic import BaseModel

from scheduler import context
from scheduler.models import BoefjeMeta


class SaveRawRequest(BaseModel):
    boefje_meta_id: str
    raw: str | bytes
    mime_types: Set[str] = frozenset()


class KittenAPI:
    def __init__(self, api: fastapi.FastAPI, ctx: context.AppContext) -> None:
        self.logger: structlog.BoundLogger = structlog.getLogger(__name__)
        self.api = api
        self.ctx = ctx

        self.api.add_api_route(
            path="/kitten/boefjemeta",
            endpoint=self.boefje_meta,
            methods=["POST"],
            response_model=BoefjeMeta,
            status_code=status.HTTP_200_OK,
            description="Get the boefje meta",
        )

        self.api.add_api_route(
            path="/kitten/raw",
            endpoint=self.save_raw,
            methods=["POST"],
            response_model=str,
            status_code=status.HTTP_200_OK,
            description="Save raw data",
        )

    def boefje_meta(self, task_data: dict[str, Any], oci_arguments: list[str]) -> BoefjeMeta:
        self.logger.info("BOEFJE META")
        self.logger.info(str(task_data))
        try:
            organization: str = task_data["organization"]

            input_ooi = task_data["input_ooi"]
            arguments = {"oci_arguments": oci_arguments}

            if input_ooi:
                arguments["input"] = self.ctx.services.octopoes.get_object_raw(organization, input_ooi)

            return BoefjeMeta(
                id=task_data["id"],
                boefje=task_data["boefje"],
                input_ooi=input_ooi,
                arguments=arguments,
                organization=organization,
                environment=self.ctx.services.katalogus.get_plugin_settings(
                    task_data["organization"], task_data["boefje"]["id"]
                ),
                started_at=None,
                ended_at=None,
            )
        except Exception as e:
            raise fastapi.HTTPException(status_code=fastapi.status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))

    def save_raw(self, req: SaveRawRequest):
        self.logger.info(str([req.boefje_meta_id, req.raw, req.mime_types]))
        return "0a79d9b1-53e2-479b-ab00-ab5de787240b"
