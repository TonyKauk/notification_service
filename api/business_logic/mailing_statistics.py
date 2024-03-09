from typing import Any

from django.db.models import Count, Q, QuerySet

from api.models import Mailing, Message


def count_messages_by_status(messages: QuerySet[Message]) -> dict[str, int]:
    """Формирует статистику из переданной выборки сообщений."""

    statistics = messages.aggregate(
        messages_sent=Count("is_sent", filter=Q(is_sent=True)),
        messages_failed=Count("is_sent", filter=Q(is_sent=False)),
    )
    messages_total = {
        "messages_total": (
            statistics["messages_sent"] + statistics["messages_failed"]
        )
    }
    return {**statistics, **messages_total}


def get_detailed_statistics(mailing: Mailing) -> dict[str, Any]:
    """Формирует статистику для одной рассылки."""

    messages = Message.objects.filter(mailing=mailing)
    statistics = count_messages_by_status(messages)
    info = {
        "tag": mailing.filter.tag.id,
        "text": mailing.message_text,
        "mobile_operator_code": mailing.filter.mobile_operator_code,
    }
    return {**info, **statistics}


def get_overall_statistics() -> dict[str, Any]:
    """Формирует статистику для выборки рассылок."""

    messages = Message.objects.all()
    statistics = count_messages_by_status(messages)
    mailings_total = {"mailings_total": Mailing.objects.all().count()}
    return {**mailings_total, **statistics}
