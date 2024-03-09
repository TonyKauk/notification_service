from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ClientViewSet, MailingViewSet

app_name = "api"

router = DefaultRouter()
router.register("clients", ClientViewSet)
router.register("mailings", MailingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
