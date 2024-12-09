from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy

from pytils.translit import slugify


class Board(models.Model):
    slug = models.SlugField(
        gettext_lazy('Слаг'),
        primary_key=True,
        unique=True,
        help_text=gettext_lazy('Только латинские буквы, цифры, `_`, `-`'),
    )
    name = models.CharField(
        gettext_lazy('Название'),
        max_length=settings.SHORT_LENGTH_CHARFIELD,
        unique=True,
        help_text=gettext_lazy('Только буквы и цифры'),
    )
    description = models.TextField(
        gettext_lazy('Описание'),
        max_length=settings.LONG_LENGTH_CHARFIELD,
        help_text=gettext_lazy('Только буквы, цифры и знаки припенания'),
        blank=True,
        default='',
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=gettext_lazy('Владелец'),
        related_name='boards',
    )
    created = models.DateTimeField(
        gettext_lazy('Дата создания'),
        auto_now_add=True,
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


    class Meta:
        abstract = True
