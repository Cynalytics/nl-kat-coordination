import httpx
from account.mixins import OrganizationView
from django.views.generic import TemplateView


class BoefjesRepoClient:
    def get_all_boefjes(self):
        response = httpx.get("http://boefjes-repo:8000/json-objects")

        response.raise_for_status()
        return response.json()


class BoefjesRepoView(OrganizationView, TemplateView):
    """View of all plugins in KAT-alogus"""

    name = "boefjes_repo"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo_client = BoefjesRepoClient()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["boefjes"] = self.repo_client.get_all_boefjes()
        return context

    pass
