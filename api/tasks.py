import requests
from celery import group, shared_task

from api.business_logic.send_message import post_message
from api.exceptions import BadStatusCodeError
from api.models import Client, Mailing, Message


@shared_task(
    bind=True,
    autoretry_for=(requests.exceptions.RequestException, BadStatusCodeError),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
)
def send_message(self, mailing_id: int, client_id: int):
    """Отправка одного запроса об отправке сообщения на внешний API."""

    mailing = Mailing.objects.get(id=mailing_id)
    client = Client.objects.get(id=client_id)
    message = Message.objects.get_or_create(mailing=mailing, client=client)[0]
    response = post_message(
        mailing=mailing, client=client, message_id=message.id
    )
    if response.status_code != 200:
        raise BadStatusCodeError
    message.is_sent = True
    message.save()


@shared_task(
    bind=True, retry_backoff=True, retry_backoff_max=60, retry_jitter=True
)
def start_mailing(self, mailing_id: int):
    """Отправка организация группы запросов об отправке сообщений
    на внешний API.
    """

    mailing = Mailing.objects.get(id=mailing_id)
    clients = Client.objects.filter(
        tag=mailing.filter.tag,
        mobile_operator_code=mailing.filter.mobile_operator_code,
    )
    tasks = []
    for client in clients:
        tasks.append(
            send_message.s(mailing_id=mailing_id, client_id=client.id).set(
                expires=mailing.end_datetime
            )
        )
    group(tasks)()
