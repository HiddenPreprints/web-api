from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls

from . import views

urlpatterns = [
    url(r"^", include(views.categories_router.urls)),
    url(r"^docs/", include_docs_urls(title="Equitable Preprints")),
    url("", include("django_prometheus.urls")),
]
