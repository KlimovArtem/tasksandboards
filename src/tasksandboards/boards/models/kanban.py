from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

from boards.models.base import Board


class Kanban(Board):
    def get_absolute_url(self):
        return reverse_lazy('boards:board_tasks', kwargs={'board_slug': self.slug})


class Column(models.Model):
    name = models.CharField(
        gettext_lazy('Колонка'),
        max_length=settings.SHORT_LENGTH_CHARFIELD,
        help_text=gettext_lazy('Только буквы и цифры'),
    )
    position = models.SmallIntegerField()
    board = models.ForeignKey(
        Kanban,
        on_delete=models.CASCADE,
        verbose_name=gettext_lazy('Доска'),
        related_name='columns',
    )

    class Meta:
        ordering = ['position']

    def __str__(self) -> str:
        return self.name


# class Tasks(models.Model):
#     title = models.CharField(
#         gettext_lazy('Загаловок'),  # noqa: ERA001
#         max_length=settings.SHORT_LENGTH_CHARFIELD,  # noqa: ERA001
#         help_text=gettext_lazy('Только буквы, цифры и знаки припенания'),  # noqa: ERA001
#     )
#     description = models.TextField(
#         gettext_lazy('Описание'),  # noqa: ERA001
#         max_length=settings.LONG_LENGTH_CHARFIELD,  # noqa: ERA001
#         help_text=gettext_lazy('Только буквы, цифры и знаки припенания'),  # noqa: ERA001
#         blank=True,  # noqa: ERA001
#         null=True,  # noqa: ERA001
#     )
#     deadline = models.DateField(
#         gettext_lazy('Крайний срок'),  # noqa: ERA001
#     )
#     status = models.ForeignKey(
#         Column,
#         verbose_name=gettext_lazy('Статус'),  # noqa: ERA001
#         related_name='tasks',  # noqa: ERA001
#     )
