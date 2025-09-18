import httpx
import structlog
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

logger = structlog.get_logger()


class BoefjeDownloadView(View):
    def get(self, request, organization_code, boefje_id):
        # 1. Prepare the payload exactly as in the cURL example
        payload = {
            "id": boefje_id,
            "name": "my boefje",
            "version": "1.0",
            "created": "2025-07-01T08:02:54.959Z",
            "description": f"{boefje_id} description",
            "enabled": False,
            "static": True,
            "type": "boefje",
            "scan_level": 1,
            "consumes": ["IPAddressV4"],
            "produces": [],
            "boefje_schema": {"title": "Arguments", "type": "object", "properties": {}, "required": []},
            "oci_image": "my_boefje",
        }

        # 2. POST to the external API
        post_url = f"http://katalogus:8000/v1/organisations/{organization_code}/plugins"
        try:
            post_resp = httpx.post(
                post_url,
                json=payload,
                headers={"Content-Type": "application/json", "accept": "application/json"},
                timeout=10,
            )
            post_resp.raise_for_status()
            logger.info("Boefje posted to katalogus", post_url=post_url, status=post_resp.status_code)
        except Exception as e:
            logger.error("Failed to post boefje to katalogus", error=str(e))
            return HttpResponse("Failed to post boefje to katalogus", status=500)

        # 3. Redirect to the katalogus view
        katalogus_url = reverse("katalogus", args=[organization_code])
        return redirect(katalogus_url)
