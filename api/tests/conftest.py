import datetime
from typing import Any, NamedTuple

import pytest
from django.utils.timezone import make_aware

from api.models import Client, Filter, Mailing, Message, Tag


@pytest.fixture
def tag_seller(db) -> Tag:
    """Фикстура тэга продавца."""

    return Tag.objects.create(name="seller")


@pytest.fixture
def tag_manager(db) -> Tag:
    """Фикстура тэга менеджера."""

    return Tag.objects.create(name="manager")


@pytest.fixture
def filter_seller_926(db, tag_seller: Tag) -> Filter:
    """Фикстура фильтра по продавцу и коду оператора 926."""

    return Filter.objects.create(mobile_operator_code=926, tag=tag_seller)


@pytest.fixture
def filter_manager_927(db, tag_manager: Tag) -> Filter:
    """Фикстура фильтра по менеджеру и коду оператора 927."""

    return Filter.objects.create(mobile_operator_code=927, tag=tag_manager)


@pytest.fixture
def mailing_seller_926_hello(db, filter_seller_926: Filter) -> Mailing:
    """Фикстура рассылки по фильтру по продавцу и коду оператора 926,
    с сообщением 'hello'.
    """

    return Mailing.objects.create(
        start_datetime=make_aware(datetime.datetime(2023, 1, 1, 1, 0, 0)),
        end_datetime=make_aware(datetime.datetime(2023, 1, 2, 1, 0, 0)),
        message_text="hello",
        filter=filter_seller_926,
    )


@pytest.fixture
def mailing_manager_927_hello(db, filter_manager_927: Filter) -> Mailing:
    """Фикстура рассылки по фильтру по менеджеру и коду оператора 927,
    с сообщением 'hello'.
    """

    return Mailing.objects.create(
        start_datetime=make_aware(datetime.datetime(2023, 1, 1, 1, 0, 0)),
        end_datetime=make_aware(datetime.datetime(2023, 1, 2, 1, 0, 0)),
        message_text="hello",
        filter=filter_manager_927,
    )


@pytest.fixture
def client_seller_926_1(db, tag_seller: Tag) -> Client:
    """Фикстура клиента с кодом оператора 926."""

    return Client.objects.create(phone_number=79261234567, tag=tag_seller)


@pytest.fixture
def client_seller_926_2(db, tag_seller: Tag) -> Client:
    """Фикстура клиента с кодом оператора 926."""

    return Client.objects.create(phone_number=79261234568, tag=tag_seller)


@pytest.fixture
def client_seller_926_3(db, tag_seller: Tag) -> Client:
    """Фикстура клиента с кодом оператора 926."""

    return Client.objects.create(phone_number=79261234569, tag=tag_seller)


@pytest.fixture
def client_manager_927_1(db, tag_manager: Tag) -> Client:
    """Фикстура клиента с кодом оператора 927."""

    return Client.objects.create(phone_number=79271234567, tag=tag_manager)


@pytest.fixture
def client_manager_927_2(db, tag_manager: Tag) -> Client:
    """Фикстура клиента с кодом оператора 927."""

    return Client.objects.create(phone_number=79271234568, tag=tag_manager)


@pytest.fixture
def client_manager_927_3(db, tag_manager: Tag) -> Client:
    """Фикстура клиента с кодом оператора 927."""

    return Client.objects.create(phone_number=79271234569, tag=tag_manager)


@pytest.fixture
def message_client_seller_926_1(
    db, client_seller_926_1: Client, mailing_seller_926_hello: Mailing
) -> Message:
    """Фикстура сообщенея клиенту по фильтру продавца и
    с кодом оператора 926.
    """

    return Message.objects.create(
        created_datetime=make_aware(datetime.datetime(2023, 1, 1, 2, 0, 0)),
        is_sent=True,
        mailing=mailing_seller_926_hello,
        client=client_seller_926_1,
    )


@pytest.fixture
def message_client_seller_926_2(
    db, client_seller_926_2: Client, mailing_seller_926_hello: Mailing
) -> Message:
    """Фикстура сообщенея клиенту по фильтру продавца и
    с кодом оператора 926.
    """

    return Message.objects.create(
        created_datetime=make_aware(datetime.datetime(2023, 1, 1, 3, 0, 0)),
        is_sent=True,
        mailing=mailing_seller_926_hello,
        client=client_seller_926_2,
    )


@pytest.fixture
def message_client_seller_926_3(
    db, client_seller_926_3: Client, mailing_seller_926_hello: Mailing
) -> Message:
    """Фикстура сообщенея клиенту по фильтру продавца и
    с кодом оператора 926.
    """

    return Message.objects.create(
        created_datetime=make_aware(datetime.datetime(2023, 1, 1, 4, 0, 0)),
        is_sent=False,
        mailing=mailing_seller_926_hello,
        client=client_seller_926_3,
    )


@pytest.fixture
def message_client_manager_927_1(
    db, client_manager_927_1: Client, mailing_manager_927_hello: Mailing
) -> Message:
    """Фикстура сообщенея клиенту по фильтру менеджера и
    с кодом оператора 927.
    """

    return Message.objects.create(
        created_datetime=make_aware(datetime.datetime(2023, 1, 1, 2, 0, 0)),
        is_sent=True,
        mailing=mailing_manager_927_hello,
        client=client_manager_927_1,
    )


@pytest.fixture
def message_client_manager_927_2(
    db, client_manager_927_2: Client, mailing_manager_927_hello: Mailing
) -> Message:
    """Фикстура сообщенея клиенту по фильтру менеджера и
    с кодом оператора 927.
    """

    return Message.objects.create(
        created_datetime=make_aware(datetime.datetime(2023, 1, 1, 3, 0, 0)),
        is_sent=True,
        mailing=mailing_manager_927_hello,
        client=client_manager_927_2,
    )


@pytest.fixture
def message_client_manager_927_3(
    db, client_manager_927_3: Client, mailing_manager_927_hello: Mailing
) -> Message:
    """Фикстура сообщенея клиенту по фильтру менеджера и
    с кодом оператора 927.
    """

    return Message.objects.create(
        created_datetime=make_aware(datetime.datetime(2023, 1, 1, 4, 0, 0)),
        is_sent=False,
        mailing=mailing_manager_927_hello,
        client=client_manager_927_3,
    )


class DetailedStatisticsFixture(NamedTuple):
    """Класс хранения фикстуры детальной статистики с ожидаемым результатом."""

    input_mailing: Mailing
    expected_result: dict[str, Any]


class OverallStatisticsFixture(NamedTuple):
    """Класс хранения фикстуры общей статистики с ожидаемым результатом."""

    expected_result: dict[str, Any]


@pytest.fixture
def detailed_statistics_seller_fixture(
    db,
    mailing_seller_926_hello: Mailing,
    message_client_seller_926_1: Message,
    message_client_seller_926_2: Message,
    message_client_seller_926_3: Message,
) -> DetailedStatisticsFixture:
    """Фикстура детальной статистики."""

    expected = {
        "messages_sent": 2,
        "messages_failed": 1,
        "messages_total": 3,
        "tag": 1,
        "text": "hello",
        "mobile_operator_code": 926,
    }
    return DetailedStatisticsFixture(
        input_mailing=mailing_seller_926_hello,
        expected_result=expected,
    )


@pytest.fixture
def overall_statistics_fixture(
    db,
    message_client_seller_926_1: Message,
    message_client_seller_926_2: Message,
    message_client_seller_926_3: Message,
    message_client_manager_927_1: Message,
    message_client_manager_927_2: Message,
    message_client_manager_927_3: Message,
) -> OverallStatisticsFixture:
    """Фикстура общей статистики."""

    expected = {
        "mailings_total": 2,
        "messages_total": 6,
        "messages_sent": 4,
        "messages_failed": 2,
    }

    return OverallStatisticsFixture(expected_result=expected)
