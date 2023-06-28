from django.db import models
from pytils.translit import slugify


class BaseMark(models.Model):
    """Базовый класс для категории и тегов."""
    name = models.CharField(
        verbose_name='Имя',
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=100,
        unique=True,
        blank=True,
    )
    created = models.DateTimeField(
        verbose_name='Создано',
        auto_now_add=True,
        auto_now=False,
    )
    modified = models.DateTimeField(
        verbose_name='Изменено',
        auto_now=True,
        auto_now_add=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            max_slug_length = self._meta.get_field('slug').max_length
            self.slug = slugify(self.name)[:max_slug_length]
        super().save(*args, **kwargs)


class TagCategory(BaseMark):

    class Meta:
        verbose_name = 'категория тегов'
        verbose_name_plural = 'Категории тегов'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(BaseMark):

    category = models.ForeignKey(
        to=TagCategory,
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ('category__name', 'name')

    def __str__(self):
        return self.name
