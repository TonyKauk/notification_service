from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.business_logic.mailing_statistics import (
    get_detailed_statistics,
    get_overall_statistics,
)
from api.mixins import ListCreateUpdateDestroyViewSet
from api.models import Client, Mailing
from api.serializers import ClientSerializer, MailingSerializer


class ClientViewSet(ListCreateUpdateDestroyViewSet):
    """Вьюсэт для эндпоинтов связанных с клиентами."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingViewSet(ListCreateUpdateDestroyViewSet):
    """Вьюсэт для эндпоинтов связанных с рассылками."""

    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    @action(
        detail=True,
        methods=["get"],
        url_path="detailed-statistics",
        url_name="detailed-statistics",
    )
    def detailed_statistics(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        statistics = get_detailed_statistics(mailing)
        return Response(data=statistics, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path="overall-statistics",
        url_name="overall-statistics",
    )
    def overall_statistics(self, request):
        statistics = get_overall_statistics()
        return Response(data=statistics, status=status.HTTP_200_OK)
