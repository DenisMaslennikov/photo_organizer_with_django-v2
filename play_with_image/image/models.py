from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from tag_anything.models import Tag
from .utils import (
    get_exif,
    get_iso,
    get_flash,
    get_f_number,
    get_lens_model,
    get_camera_model,
    get_exposure_time,
    get_focal_length,
    get_average_image_hash,
    get_longitude,
    get_latitude,
    logger,
)

User = get_user_model()


class Image(models.Model):

    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='img/%Y/%m/%d',
    )

    author = models.ForeignKey(
        to=User,
        verbose_name='Автор',
        on_delete=models.CASCADE,

    )

    tags = models.ManyToManyField(to=Tag, verbose_name='Теги')

    created = models.DateTimeField(
        verbose_name='Загружено',
        auto_now_add=True,
        auto_now=False,
    )

    modified = models.DateTimeField(
        verbose_name='Обновлено',
        auto_now_add=False,
        auto_now=True,
    )

    name = models.CharField(max_length=255, verbose_name='Название')

    image_hash = models.CharField(
        max_length=16,
        verbose_name='Хеш изображения',
        editable=False,
        null=True,
    )

    image_hash_part1 = models.IntegerField(
        verbose_name='Хеш 1/4',
        editable=False,
        null=True,
    )

    image_hash_part2 = models.IntegerField(
        verbose_name='Хеш 2/4',
        editable=False,
        null=True,
    )

    image_hash_part3 = models.IntegerField(
        verbose_name='Хеш 3/4',
        editable=False,
        null=True,
    )

    image_hash_part4 = models.IntegerField(
        verbose_name='Хеш 4/4',
        editable=False,
        null=True,
    )

    private = models.BooleanField(
        verbose_name='Приватное',
        default=False,
    )

    camera_model = models.CharField(
        max_length=255,
        verbose_name='Камера',
        null=True,
    )

    lens_model = models.CharField(
        max_length=255,
        verbose_name='Объектив',
        null=True,
    )

    iso = models.PositiveIntegerField(
        verbose_name='ISO',
        null=True,
    )

    focal_length = models.FloatField(
        verbose_name='Фокусное Расстояние',
        null=True,
    )

    flash = models.BooleanField(
        verbose_name='Вспышка',
        null=True,
    )

    f = models.FloatField(
        verbose_name='Диафрагма',
        null=True,
    )

    exposure_time = models.CharField(
        verbose_name='Время Экспозиции',
        max_length=10,
        null=True,
    )

    longitude = models.CharField(
        verbose_name='Долгота',
        max_length=11,
        null=True,
    )

    latitude = models.CharField(
        verbose_name='Широта',
        max_length=11,
        null=True,
    )

    class Meta:
        default_related_name = 'images'
        verbose_name = 'изображение'
        verbose_name_plural = 'Изображения'
        ordering = ('-created', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gallery:image', args=(self.pk, ))

    def save(self, *args, **kwargs):
        logger.debug('Сохранение изображения')
        super().save(*args, **kwargs)
        if (
                self.image.path.endswith('.jpg')
                or self.image.path.endswith('.jpeg')
        ):
            try:
                logger.debug('Читаем EXIF')
                image_exif = get_exif(self.image.path)
                self.camera_model = get_camera_model(image_exif)
                self.lens_model = get_lens_model(image_exif)
                self.iso = get_iso(image_exif)
                self.focal_length = get_focal_length(image_exif)
                self.flash = bool(get_flash(image_exif))
                self.f = get_f_number(image_exif)
                self.exposure_time = get_exposure_time(image_exif)
                self.longitude = get_longitude(image_exif)
                self.latitude = get_latitude(image_exif)
            except Exception as error:
                logger.error(error, exc_info=True)
        if not self.image_hash:
            logger.debug('Определяем хеш изображения')
            self.image_hash = str(get_average_image_hash(self.image.path))
            self.image_hash_part1 = int(self.image_hash[:4], 16)
            self.image_hash_part2 = int(self.image_hash[4:8], 16)
            self.image_hash_part3 = int(self.image_hash[8:12], 16)
            self.image_hash_part4 = int(self.image_hash[12:16], 16)
        super().save(*args, **kwargs)
