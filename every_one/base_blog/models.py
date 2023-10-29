from datetime import datetime

from django.db import models
from django.utils import timezone


# Create your models here.

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

    choice_month = models.IntegerField(default=True)

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
