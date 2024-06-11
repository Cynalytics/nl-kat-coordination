import logging

import httpx

logger = logging.getLogger("katty")


def toggle_plugin(organisation_id: str, plugin_id: str):
    katalogus_client = httpx.Client(
        base_url="http://localhost:8003",
        follow_redirects=True,
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )

    plugin_response = katalogus_client.get(f"/v1/organisations/{organisation_id}/plugins/{plugin_id}")

    if plugin_response.is_error:
        logger.error("Something went wrong with getting the %s plugin\n%s", plugin_id, plugin_response.text)
        return

    response = katalogus_client.patch(
        f"/v1/organisations/{organisation_id}/repositories/LOCAL/plugins/{plugin_id}",
        json={"enabled": not plugin_response.json()["enabled"]},
    )

    if response.is_error:
        logger.error("Something went wrong with toggling the %s plugin\n%s", plugin_id, response.text)
        return
    action = "disabled" if plugin_response.json()["enabled"] else "enabled"
    logger.info("The %s plugin has been successfully %s!", plugin_id, action)
