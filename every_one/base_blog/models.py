from datetime import datetime

from django.db import models
from django.db.models import DateTimeField


# Create your models here.
class Admin(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='ID пользователя',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Имя пользователя',
    )


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='ID пользователя',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Имя пользователя',
    )
    time_create = models.DateTimeField(default=datetime.now(),
                                       verbose_name='Дата регистрации'
                                       )
    time_update = models.DateTimeField(default=datetime.now())

    choice_month = models.DateTimeField(null=True)

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Event(models.Model):
    name_event = models.CharField(max_length=60,
                                  verbose_name='Эвент'
                                  )
    info_event = models.CharField(max_length=700,
                                  verbose_name='Информация',
                                  default=True
                                  )

    user_create = models.ForeignKey(Profile,
                                    on_delete=models.CASCADE,
                                    null=True
                                    )

    start_time: DateTimeField = models.DateTimeField(verbose_name='Время начала',
                                                     null=True)
    create_time = models.DateTimeField(default=datetime.now)
    publish = models.BooleanField(default=False,
                                  verbose_name='Опубликовано')
    url = models.CharField(max_length=200,
                           verbose_name='Ссылка',
                           null=True,
                           default='Нет ссылки')

    class Meta:
        verbose_name = 'Эвент'
        verbose_name_plural = 'Эвенты'


class EventIsRead(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    read_date = models.DateTimeField(auto_now_add=True)
