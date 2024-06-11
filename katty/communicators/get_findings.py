import json
import logging
from datetime import datetime, timezone

import httpx

logger = logging.getLogger("katty")


def get_findings(organisation_id: str):
    bytes_client = httpx.Client(
        base_url="http://localhost:8001", follow_redirects=True, headers={"accept": "application/json"}
    )

    severities = ["medium", "high", "critical"]
    response = bytes_client.get(
        f"/{organisation_id}/objects",
        params={"severities": severities, "valid_time": str(datetime.now(timezone.utc)), "types": "FindingType"},
    )
    if response.is_error:
        return logger.error("Something went wrong with getting the findings\n%s", response.text)

    formatted = [{"type": x["id"], "score": x["risk_score"]} for x in response.json()["items"]]
    logger.info("%s | RAW: %s", formatted, json.dumps(formatted, sort_keys=True, indent=2))
