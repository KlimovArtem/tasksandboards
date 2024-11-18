from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy

from boards.models.base import Board


class Kanban(Board):
    pass


class Column(models.Model):
    name = models.CharField(
        gettext_lazy('Колонка'),
        max_length=settings.SHORT_LENGTH_CHARFIELD,
        help_text=gettext_lazy('Только буквы и цифры')
    )
    position = models.SmallIntegerField()
    board = models.ForeignKey(
        Kanban,
        on_delete=models.CASCADE,
        verbose_name=gettext_lazy('Доска'),
        related_name='columns'
    )

    class Meta:
        ordering = ['position']


# class Tasks(models.Model):
#     title = models.CharField(
#         gettext_lazy('Загаловок'),
#         max_length=settings.SHORT_LENGTH_CHARFIELD,
#         help_text=gettext_lazy('Только буквы, цифры и знаки припенания'),
#     )
#     description = models.TextField(
#         gettext_lazy('Описание'),
#         max_length=settings.LONG_LENGTH_CHARFIELD,
#         help_text=gettext_lazy('Только буквы, цифры и знаки припенания'),
#         blank=True,
#         null=True,
#     )
#     deadline = models.DateField(
#         gettext_lazy('Крайний срок'),
#     )
#     status = models.ForeignKey(
#         Column,
#         verbose_name=gettext_lazy('Статус'),
#         related_name='tasks',
#     )