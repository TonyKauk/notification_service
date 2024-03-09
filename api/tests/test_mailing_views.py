import datetime
import json
from typing import Any

import pytest
from django.urls import reverse
from django_celery_beat.models import PeriodicTask
from rest_framework import status

from api.models import Filter, Mailing
from api.tests.conftest import (
    DetailedStatisticsFixture,
    OverallStatisticsFixture,
)


@pytest.fixture
def mailing_seller_926_hello_fixture(
    db, mailing_seller_926_hello: Mailing, filter_seller_926: Filter
) -> dict[str:Any]:
    """Создание фикстуры рассылки с фильтром по коду 926 и тэгу продавца и
    подготовка ожидаемого результат.
    """

    return {
        "id": 1,
        "start_datetime": "2023-01-01T01:00:00Z",
        "end_datetime": "2023-01-02T01:00:00Z",
        "message_text": "hello",
        "filter": {
            "id": 1,
            "mobile_operator_code": 926,
            "tag": {"id": 1, "name": "seller"},
        },
    }


def test_mailing_list(
    db, client, mailing_seller_926_hello_fixture: dict[str:Any]
):
    """Тест на корректное формирование списка рассылок."""

    url = reverse("api:mailing-list")
    response = client.get(url)
    assert json.loads(response.content) == [mailing_seller_926_hello_fixture]


def test_mailing_detail(
    db, client, mailing_seller_926_hello_fixture: dict[str:Any]
):
    """Тест на недоступность эндпоинта с детальной информации
    об отдельной рассылке.
    """

    url = reverse("api:mailing-detail", kwargs={"pk": 1})
    response = client.get(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_mailing_create(db, client):
    """Тест на корректное создание рассылки."""

    url = reverse("api:mailing-list")
    response = client.post(
        url,
        data={
            "start_datetime": "2023-01-01T20:00",
            "end_datetime": "2023-01-01T20:05",
            "message_text": "hi",
            "filter": {"tag": {"name": "seller"}, "mobile_operator_code": 926},
        },
        content_type="application/json",
    )
    assert json.loads(response.content) == {
        "id": 1,
        "start_datetime": "2023-01-01T20:00:00Z",
        "end_datetime": "2023-01-01T20:05:00Z",
        "message_text": "hi",
        "filter": {
            "id": 1,
            "mobile_operator_code": 926,
            "tag": {"id": 1, "name": "seller"},
        },
    }


def test_mailing_scheduled(db, client):
    """Тест на корректное создание задания по рассылке."""

    url = reverse("api:mailing-list")
    client.post(
        url,
        data={
            "start_datetime": "2025-01-01T20:00",
            "end_datetime": "2025-01-01T20:05",
            "message_text": "hi",
            "filter": {"tag": {"name": "seller"}, "mobile_operator_code": 926},
        },
        content_type="application/json",
    )
    assert (
        PeriodicTask.objects.filter(
            kwargs__icontains='"mailing_id": 1'
        ).exists()
        is True
    )


def test_mailing_put(db, client, mailing_seller_926_hello: Mailing):
    """Тест на корректное изменение рассылки."""

    url = reverse("api:mailing-detail", kwargs={"pk": 1})
    response = client.put(
        url,
        data={
            "start_datetime": "2025-01-01T01:00:01",
            "end_datetime": "2028-01-02T01:00:01",
            "message_text": "hello!",
            "filter": {
                "mobile_operator_code": 927,
                "tag": {"name": "seller!"},
            },
        },
        content_type="application/json",
    )
    assert json.loads(response.content) == {
        "id": 1,
        "start_datetime": "2025-01-01T01:00:01Z",
        "end_datetime": "2028-01-02T01:00:01Z",
        "message_text": "hello!",
        "filter": {
            "id": 2,
            "mobile_operator_code": 927,
            "tag": {"id": 2, "name": "seller!"},
        },
    }


def test_mailing_put_schedule(db, client, mailing_seller_926_hello: Mailing):
    """Тест на корректное изменение задания по рассылке."""

    url = reverse("api:mailing-detail", kwargs={"pk": 1})
    client.put(
        url,
        data={
            "start_datetime": "2025-01-01T01:00:01",
            "end_datetime": "2028-01-02T01:00:01",
            "message_text": "hello!",
            "filter": {
                "mobile_operator_code": 927,
                "tag": {"name": "seller!"},
            },
        },
        content_type="application/json",
    )
    updated_scheduled_mailing = PeriodicTask.objects.get(
        kwargs__icontains='"mailing_id": 1'
    )
    assert updated_scheduled_mailing.clocked.clocked_time == datetime.datetime(
        2025, 1, 1, 1, 0, 1, tzinfo=datetime.timezone.utc
    )


def test_mailing_patch(db, client, mailing_seller_926_hello: Mailing):
    """Тест на корректное изменение рассылки."""

    url = reverse("api:mailing-detail", kwargs={"pk": 1})
    response = client.patch(
        url,
        data={
            "start_datetime": "2023-01-01T01:00:01",
            "end_datetime": "2023-01-02T01:00:01",
            "message_text": "hello!",
            "filter": {
                "mobile_operator_code": 927,
                "tag": {"name": "seller!"},
            },
        },
        content_type="application/json",
    )
    assert json.loads(response.content) == {
        "id": 1,
        "start_datetime": "2023-01-01T01:00:01Z",
        "end_datetime": "2023-01-02T01:00:01Z",
        "message_text": "hello!",
        "filter": {
            "id": 2,
            "mobile_operator_code": 927,
            "tag": {"id": 2, "name": "seller!"},
        },
    }


def test_mailing_patch_schedule(db, client, mailing_seller_926_hello: Mailing):
    """Тест на корректное изменение задания по рассылке."""

    url = reverse("api:mailing-detail", kwargs={"pk": 1})
    client.patch(
        url,
        data={
            "start_datetime": "2025-01-01T01:00:01",
            "end_datetime": "2028-01-02T01:00:01",
            "message_text": "hello!",
            "filter": {
                "mobile_operator_code": 927,
                "tag": {"name": "seller!"},
            },
        },
        content_type="application/json",
    )
    updated_scheduled_mailing = PeriodicTask.objects.get(
        kwargs__icontains='"mailing_id": 1'
    )
    assert updated_scheduled_mailing.clocked.clocked_time == datetime.datetime(
        2025, 1, 1, 1, 0, 1, tzinfo=datetime.timezone.utc
    )


def test_mailing_delete(db, client, mailing_seller_926_hello: Mailing):
    """Тест на корректное удаление рассылки."""

    url = reverse("api:mailing-detail", kwargs={"pk": 1})
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_mailing_delete_schedule(db, client, mailing_seller_926_hello: Mailing):
    """Тест на корректное удаление задания по рассылке."""

    url = reverse("api:mailing-detail", kwargs={"pk": 1})
    client.delete(url)
    assert (
        PeriodicTask.objects.filter(
            kwargs__icontains='"mailing_id": 1'
        ).exists()
        is False
    )


def test_mailing_detailed_statistics(
    db, client, detailed_statistics_seller_fixture: DetailedStatisticsFixture
):
    """Тест на формирование детальной статистики."""

    url = reverse("api:mailing-detailed-statistics", kwargs={"pk": 1})
    response = client.get(url)
    assert (
        json.loads(response.content)
        == detailed_statistics_seller_fixture.expected_result
    )


def test_mailing_overall_statistics(
    db, client, overall_statistics_fixture: OverallStatisticsFixture
):
    """Тест на формирование общей статистики."""

    url = reverse("api:mailing-overall-statistics")
    response = client.get(url)
    assert (
        json.loads(response.content)
        == overall_statistics_fixture.expected_result
    )
