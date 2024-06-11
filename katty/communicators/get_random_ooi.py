import json
import logging

import httpx

logger = logging.getLogger("katty")


def get_random_ooi(organisation_id: str):
    client = httpx.Client(base_url="http://localhost:8001", follow_redirects=True)
    response = client.get(
        f"/{organisation_id}/objects/random", params=[("amount", "1"), ("valid_time", "2024-06-06T11:34:47Z")]
    )

    logger.info("%s | RAW: %s", response, json.dumps(response.json(), sort_keys=True, indent=2))
