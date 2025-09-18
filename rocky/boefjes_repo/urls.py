from django.urls import path

from boefjes_repo.views.boefje_download import BoefjeDownloadView
from boefjes_repo.views.boefjes_repo import BoefjesRepoView

urlpatterns = [
    path("", BoefjesRepoView.as_view(template_name="boefjes_repo/boefjes_repo.html"), name="organization_boefjes_repo"),
    path("download/<str:boefje_id>/", BoefjeDownloadView.as_view(), name="boefje_download"),
]
