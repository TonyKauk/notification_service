import os

import requests
from dotenv import load_dotenv, find_dotenv

from api.models import Mailing, Client

load_dotenv(find_dotenv())

BASE_URL = os.environ["BASE_URL"]
TOKEN = os.environ["TOKEN"]


def post_message(
    mailing: Mailing, client: Client, message_id: int
) -> requests.Response:
    """Отправляет на внешний API запрос об отправке сообщения в соответствии с
    рассылкой.
    """

    headers = {"Authorizatioin": TOKEN}
    json = {
        "id": message_id,
        "phone": client.phone_number,
        "text": mailing.message_text,
    }
    url = BASE_URL + f"/{message_id}"
    return requests.post(url=url, headers=headers, json=json, timeout=(5, 5))
