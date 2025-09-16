from django.urls import path

from boefjes_repo.views.boefjes_repo import BoefjesRepoView

urlpatterns = [
    path("", BoefjesRepoView.as_view(template_name="boefjes_repo/boefjes_repo.html"), name="organization_boefjes_repo")
]
