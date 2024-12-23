from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy

from boards.models import kanban

class Task(models.Model):
    title = models.CharField(
        max_length=settings.SHORT_LENGTH_CHARFIELD,
        verbose_name=gettext_lazy('Загаловок'),
        help_text=gettext_lazy('Только буквы и знаки препинания.'),
    )
    body = models.CharField(
        max_length=settings.LONG_LENGTH_CHARFIELD,
        verbose_name=gettext_lazy('Описание'),
        help_text=gettext_lazy('Только буквы и знаки препинания.'),
        blank=True,
    )
    deadline = models.DateTimeField(
        verbose_name=gettext_lazy('Дедлайн'),
        help_text=gettext_lazy('Не может быть меньше текущей даты.')
    )
    board = models.ForeignKey(
        kanban.Kanban,
        verbose_name=gettext_lazy('Доска'),
        help_text=gettext_lazy('Обязательное! Должен быт доской типа канбан.'),
        on_delete=models.CASCADE,
    )
    status = models.ForeignKey(
        kanban.Column,
        verbose_name=gettext_lazy('Статус'),
        help_text=gettext_lazy('Должен соотносится с существующей колонкой и доской или быть Null'),
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )
