import json
from typing import Any

import pytest
from django.urls import reverse
from rest_framework import status

from api.models import Client, Tag


@pytest.fixture
def client_seller_926_1_fixture(
    db, client_seller_926_1: Client, tag_seller: Tag
) -> dict[str:Any]:
    """Создание фикстуры продавца с кодом 926, тэга продавца и подготовка
    ожидаемого результат.
    """

    return {
        "id": 1,
        "phone_number": 79261234567,
        "mobile_operator_code": 926,
        "tag": {"id": 1, "name": "seller"},
    }


def test_client_list(db, client, client_seller_926_1_fixture: dict[str:Any]):
    """Тест на корректное формирование списка клиентов."""

    url = reverse("api:client-list")
    response = client.get(url)
    assert json.loads(response.content) == [client_seller_926_1_fixture]


def test_client_detail(db, client, client_seller_926_1: Client):
    """Тест на недоступность эндпоинта с детальной информации
    об отдельном клиенте.
    """

    url = reverse("api:client-detail", kwargs={"pk": 1})
    response = client.get(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_client_create(db, client):
    """Тест на корректное создание клиента."""

    url = reverse("api:client-list")
    response = client.post(
        url,
        data={
            "phone_number": 79261234567,
            "tag": {"name": "seller"},
        },
        content_type="application/json",
    )
    assert json.loads(response.content) == {
        "id": 1,
        "phone_number": 79261234567,
        "mobile_operator_code": 926,
        "tag": {"id": 1, "name": "seller"},
    }


def test_client_put(db, client, client_seller_926_1: Client):
    """Тест на корректное редактирование клиента."""

    url = reverse("api:client-detail", kwargs={"pk": 1})
    response = client.put(
        url,
        data={
            "phone_number": 79291234599,
            "tag": {"name": "sellers"},
        },
        content_type="application/json",
    )
    assert json.loads(response.content) == {
        "id": 1,
        "phone_number": 79291234599,
        "mobile_operator_code": 929,
        "tag": {"id": 2, "name": "sellers"},
    }


def test_client_patch(db, client, client_seller_926_1: Client):
    """Тест на корректное редактирование клиента."""

    url = reverse("api:client-detail", kwargs={"pk": 1})
    response = client.patch(
        url,
        data={
            "phone_number": 79291234599,
            "tag": {"name": "sellers"},
        },
        content_type="application/json",
    )
    assert json.loads(response.content) == {
        "id": 1,
        "phone_number": 79291234599,
        "mobile_operator_code": 929,
        "tag": {"id": 2, "name": "sellers"},
    }


def test_client_delete(db, client, client_seller_926_1: Client):
    """Тест на корректное удаление клиента."""

    url = reverse("api:client-detail", kwargs={"pk": 1})
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
