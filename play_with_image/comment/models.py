from django.contrib.auth import get_user_model
from django.db import models

from image.models import Image


User = get_user_model()


class Comment(models.Model):

    created = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True,
        auto_now=False,
    )

    modified = models.DateTimeField(
        verbose_name='Отредактирован',
        auto_now=True,
        auto_now_add=False,
    )

    text = models.TextField(verbose_name='Комментарий')

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    image = models.ForeignKey(
        to=Image,
        on_delete=models.CASCADE,
        verbose_name='Изображение',
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)
