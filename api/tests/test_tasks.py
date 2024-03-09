import datetime
import time

import pytest
import requests
from django.utils.timezone import make_aware

from api.models import Client, Filter, Mailing, Message
from api.tasks import start_mailing


@pytest.fixture(scope="session")
def celery_config():
    """Настройки для тестового приложения Celery."""

    return {"task_always_eager": True}


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Защита от выполнения запросов библиотекой requests во время проведения
    тестов."""

    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture
def mailing_seller_926_hello_future(db, filter_seller_926: Filter) -> Mailing:
    """Фикстура рассылки в будущем."""

    return Mailing.objects.create(
        start_datetime=make_aware(
            datetime.datetime.now() + datetime.timedelta(seconds=2)
        ),
        end_datetime=make_aware(
            datetime.datetime.now() + datetime.timedelta(seconds=4)
        ),
        message_text="hello",
        filter=filter_seller_926,
    )


@pytest.fixture
def mailing_seller_926_hello_started(db, filter_seller_926: Filter) -> Mailing:
    """Фикстура рассылки, которая уже началась."""

    return Mailing.objects.create(
        start_datetime=make_aware(
            datetime.datetime.now() - datetime.timedelta(seconds=2)
        ),
        end_datetime=make_aware(
            datetime.datetime.now() + datetime.timedelta(seconds=4)
        ),
        message_text="hello",
        filter=filter_seller_926,
    )


@pytest.fixture
def mailing_seller_926_hello_past(db, filter_seller_926: Filter) -> Mailing:
    """Фикстура рассылки, которая уже закончилась."""

    return Mailing.objects.create(
        start_datetime=make_aware(
            datetime.datetime.now() - datetime.timedelta(seconds=4)
        ),
        end_datetime=make_aware(
            datetime.datetime.now() + datetime.timedelta(seconds=2)
        ),
        message_text="hello",
        filter=filter_seller_926,
    )


@pytest.fixture
def mock_response_ok(monkeypatch):
    """Мок запроса на внешний API по отправке сообщения, имитирует успешный
    запрос."""

    class MockResponseOk:
        def __init__(self):
            self.status_code = 200

    def mock_post(*args, **kwargs):
        return MockResponseOk()

    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def mock_response_bad(monkeypatch):
    """Мок запроса на внешний API по отправке сообщения, имитирует безуспешнеый
    запрос."""

    class MockResponseBad:
        def __init__(self):
            self.status_code = 400

    def mock_post(*args, **kwargs):
        return MockResponseBad()

    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def mock_response_exception(monkeypatch):
    """Мок запроса на внешний API по отправке сообщения, имитирует
    возникновение исключения библиотеки requsts (проблемы с внешним API)."""

    def mock_post(*args, **kwargs):
        raise requests.exceptions.RequestException

    monkeypatch.setattr(requests, "post", mock_post)


def test_start_mailing_ok(
    db,
    celery_app,
    celery_worker,
    mailing_seller_926_hello_future: Mailing,
    client_seller_926_1: Client,
    client_seller_926_2: Client,
    client_seller_926_3: Client,
    mock_response_ok,
):
    """Тест на успешную отправку сообщений планировщиком задач."""

    start_mailing.delay(mailing_seller_926_hello_future.id)
    time.sleep(5)
    message_count = Message.objects.filter(
        is_sent=True,
        client__in=[
            client_seller_926_1,
            client_seller_926_2,
            client_seller_926_3,
        ],
        mailing=mailing_seller_926_hello_future,
    ).count()
    assert message_count == 3


def test_start_mailing_bad(
    db,
    celery_app,
    celery_worker,
    mailing_seller_926_hello_future: Mailing,
    client_seller_926_1: Client,
    client_seller_926_2: Client,
    client_seller_926_3: Client,
    mock_response_bad,
):
    """Тест на безуспешную отправку сообщений планировщиком задач при
    400 статусе ответа внешнего API."""

    start_mailing.delay(mailing_seller_926_hello_future.id)
    time.sleep(5)
    message_count = Message.objects.filter(
        is_sent=False,
        client__in=[
            client_seller_926_1,
            client_seller_926_2,
            client_seller_926_3,
        ],
        mailing=mailing_seller_926_hello_future,
    ).count()
    assert message_count == 3


def test_start_mailing_exception(
    db,
    celery_app,
    celery_worker,
    mailing_seller_926_hello_future: Mailing,
    client_seller_926_1: Client,
    client_seller_926_2: Client,
    client_seller_926_3: Client,
    mock_response_exception,
):
    """Тест на безуспешную отправку сообщений планировщиком задач при
    возникновении исключения библиотеки requsts (проблемы с внешним API).
    """

    start_mailing.delay(mailing_seller_926_hello_future.id)
    time.sleep(5)
    message_count = Message.objects.filter(
        is_sent=False,
        client__in=[
            client_seller_926_1,
            client_seller_926_2,
            client_seller_926_3,
        ],
        mailing=mailing_seller_926_hello_future,
    ).count()
    assert message_count == 3


def test_start_mailing_on_schedule_future(
    db,
    celery_app,
    celery_worker,
    mailing_seller_926_hello_future: Mailing,
    client_seller_926_1: Client,
    client_seller_926_2: Client,
    client_seller_926_3: Client,
    mock_response_ok,
):
    """Тест на успешную отправку сообщений планировщиком задач в будущем."""

    start_mailing.delay(mailing_seller_926_hello_future.id)
    time.sleep(5)
    message_count = Message.objects.filter(
        is_sent=True,
        client__in=[
            client_seller_926_1,
            client_seller_926_2,
            client_seller_926_3,
        ],
        mailing=mailing_seller_926_hello_future,
    ).count()
    assert message_count == 3


def test_start_mailing_on_schedule_started(
    db,
    celery_app,
    celery_worker,
    mailing_seller_926_hello_started: Mailing,
    client_seller_926_1: Client,
    client_seller_926_2: Client,
    client_seller_926_3: Client,
    mock_response_ok,
):
    """Тест на успешную отправку сообщений планировщиком задач при создании
    рассылки, стартовое время которой уже наступило.
    """

    start_mailing.delay(mailing_seller_926_hello_started.id)
    time.sleep(5)
    message_count = Message.objects.filter(
        is_sent=True,
        client__in=[
            client_seller_926_1,
            client_seller_926_2,
            client_seller_926_3,
        ],
        mailing=mailing_seller_926_hello_started,
    ).count()
    assert message_count == 3


def test_start_mailing_on_schedule_past(
    db,
    celery_app,
    celery_worker,
    mailing_seller_926_hello_past: Mailing,
    client_seller_926_1: Client,
    client_seller_926_2: Client,
    client_seller_926_3: Client,
    mock_response_ok,
):
    """Тест на отсутствие отправленных сообщений планировщиком задач при
    создании рассылки, период которой уже прошел.
    """

    start_mailing.delay(mailing_seller_926_hello_past.id)
    time.sleep(5)
    message_count = Message.objects.filter(
        is_sent=False,
        client__in=[
            client_seller_926_1,
            client_seller_926_2,
            client_seller_926_3,
        ],
        mailing=mailing_seller_926_hello_past,
    ).count()
    assert message_count == 0
