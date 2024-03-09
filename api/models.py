import json

from django_celery_beat.models import ClockedSchedule, PeriodicTask
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Tag(models.Model):
    """Модель для тэга, который присваивается клиенту."""

    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name


class Filter(models.Model):
    """Модель для фильтра."""

    mobile_operator_code = models.IntegerField(
        verbose_name="Код мобильного оператора"
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        related_name="filters",
        blank=True,
        null=True,
        verbose_name="Тэг",
    )

    class Meta:
        unique_together = ("mobile_operator_code", "tag")
        verbose_name = "Фильтр"
        verbose_name_plural = "Фильтры"

    def __str__(self):
        return f"{self.tag} - {self.mobile_operator_code}"


class Mailing(models.Model):
    """Модель рассылки."""

    TASK_NAME = "Mailing"

    start_datetime = models.DateTimeField(verbose_name="Дата и время начала")
    end_datetime = models.DateTimeField(verbose_name="Дата и время окончания")
    message_text = models.TextField(verbose_name="Текст сообщения")
    filter = models.ForeignKey(
        Filter,
        on_delete=models.SET_NULL,
        related_name="mailings",
        blank=True,
        null=True,
        verbose_name="Фильтр",
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return (
            f"{self.start_datetime} - {self.end_datetime} - {self.message_text}"
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            periodic_task = PeriodicTask.objects.get(
                kwargs__icontains=f'"mailing_id": {self.id}'
            )
            periodic_task.clocked.clocked_time = self.start_datetime
            periodic_task.clocked.save()
        except models.ObjectDoesNotExist:
            schedule = ClockedSchedule.objects.create(
                clocked_time=self.start_datetime
            )
            PeriodicTask.objects.create(
                clocked=schedule,
                name=(self.TASK_NAME + f" {self.id}"),
                task="api.tasks.start_mailing",
                kwargs=json.dumps(
                    {
                        "mailing_id": self.id,
                    }
                ),
                expires=self.end_datetime,
                one_off=True,
            )
        return self

    def delete(self, *args, **kwargs):
        PeriodicTask.objects.get(
            kwargs__icontains=f'"mailing_id": {self.id}'
        ).delete()
        return super().delete(*args, **kwargs)


class Client(models.Model):
    """Модель клиента."""

    phone_number = models.IntegerField(
        validators=[
            MaxValueValidator(79999999999),
            MinValueValidator(70000000000),
        ],
        unique=True,
        verbose_name="Номер телефона",
    )
    mobile_operator_code = models.IntegerField(
        blank=True, verbose_name="Код мобильного оператора"
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        related_name="clients",
        blank=True,
        null=True,
        verbose_name="Тэг",
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        self.mobile_operator_code = int(str(self.phone_number)[1:4])
        return models.Model.save(self, *args, **kwargs)


class Message(models.Model):
    """Модель сообщения."""

    created_datetime = models.DateTimeField(
        auto_now=True, verbose_name="Дата и время создания"
    )
    is_sent = models.BooleanField(default=False, verbose_name="Отправлено")
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Рассылка",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Клиент",
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"{self.created_datetime}"
