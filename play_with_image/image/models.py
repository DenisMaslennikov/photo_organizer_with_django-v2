import logging
import os

from sorl.thumbnail import delete as delete_image_and_cache
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.urls import reverse

from tag_anything.models import Tag

from .utils import (
    get_average_image_hash,
    get_camera_model,
    get_exif,
    get_exposure_time,
    get_f_number,
    get_flash,
    get_focal_length,
    get_iso,
    get_latitude,
    get_lens_model,
    get_longitude
)

User = get_user_model()
logger = logging.getLogger(__package__)


class Image(models.Model):
    """Модель изображение"""
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="img/%Y/%m/%d",
    )

    author = models.ForeignKey(
        to=User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        editable=False,
    )

    tags = models.ManyToManyField(
        to=Tag,
        verbose_name="Теги",
        through="ImageTag",
        null=True,
    )

    created = models.DateTimeField(
        verbose_name="Загружено",
        auto_now_add=True,
        auto_now=False,
        editable=False,
    )

    modified = models.DateTimeField(
        verbose_name="Обновлено",
        auto_now_add=False,
        auto_now=True,
        editable=False,
    )

    name = models.CharField(max_length=255, verbose_name="Название")

    image_hash = models.CharField(
        max_length=16,
        verbose_name="Хеш изображения",
        editable=False,
        null=True,
    )

    image_hash_part1 = models.IntegerField(
        verbose_name="Хеш 1/4",
        editable=False,
        null=True,
    )

    image_hash_part2 = models.IntegerField(
        verbose_name="Хеш 2/4",
        editable=False,
        null=True,
    )

    image_hash_part3 = models.IntegerField(
        verbose_name="Хеш 3/4",
        editable=False,
        null=True,
    )

    image_hash_part4 = models.IntegerField(
        verbose_name="Хеш 4/4",
        editable=False,
        null=True,
    )

    private = models.BooleanField(
        verbose_name="Приватное",
        default=False,
    )

    camera_model = models.CharField(
        max_length=255,
        verbose_name="Камера",
        null=True,
        editable=False,
    )

    lens_model = models.CharField(
        max_length=255,
        verbose_name="Объектив",
        null=True,
        editable=False,
    )

    iso = models.PositiveIntegerField(
        verbose_name="ISO",
        null=True,
        editable=False,
    )

    focal_length = models.FloatField(
        verbose_name="Фокусное Расстояние",
        null=True,
        editable=False,
    )

    flash = models.BooleanField(
        verbose_name="Вспышка",
        null=True,
        editable=False,
    )

    f = models.FloatField(
        verbose_name="Диафрагма",
        null=True,
        editable=False,
    )

    exposure_time = models.CharField(
        verbose_name="Время Экспозиции",
        max_length=10,
        null=True,
        editable=False,
    )

    longitude = models.CharField(
        verbose_name="Долгота",
        max_length=11,
        null=True,
        editable=False,
    )

    latitude = models.CharField(
        verbose_name="Широта",
        max_length=11,
        null=True,
        editable=False,
    )

    class Meta:
        default_related_name = "images"
        verbose_name = "изображение"
        verbose_name_plural = "Изображения"
        ordering = ("-created",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("gallery:image", args=(self.pk,))

    def save(self, *args, **kwargs):
        logger.debug("Сохранение изображения")
        super().save(*args, **kwargs)
        # Если изображение jpg получаем информацию из EXIF
        if self.image.path.endswith(".jpg") or self.image.path.endswith(
            ".jpeg"
        ):
            try:
                logger.debug("Читаем EXIF")
                image_exif = get_exif(self.image.path)
                self.camera_model = get_camera_model(image_exif)
                self.lens_model = get_lens_model(image_exif)
                self.iso = get_iso(image_exif)
                self.focal_length = get_focal_length(image_exif)
                self.flash = get_flash(image_exif)
                self.f = get_f_number(image_exif)
                self.exposure_time = get_exposure_time(image_exif)
                self.longitude = get_longitude(image_exif)
                self.latitude = get_latitude(image_exif)
            except Exception as error:
                logger.warning(error, exc_info=True)
        # Если Хеша нет сохраняем хеш
        if not self.image_hash:
            logger.debug("Определяем хеш изображения")
            self.image_hash = str(get_average_image_hash(self.image.path))
            self.image_hash_part1 = int(self.image_hash[:4], 16)
            self.image_hash_part2 = int(self.image_hash[4:8], 16)
            self.image_hash_part3 = int(self.image_hash[8:12], 16)
            self.image_hash_part4 = int(self.image_hash[12:16], 16)


@receiver(models.signals.post_delete, sender=Image)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """Удаляем изображение и кеш с жесткого диска когда соответствующий объект
    Image удаляется"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            delete_image_and_cache(instance.image)


@receiver(models.signals.pre_save, sender=Image)
def auto_delete_old_image_on_change(sender, instance, **kwargs):
    """Удаляем старый файл изображения и кеш с диска если загружен новый"""
    if not instance.pk:
        return False
    try:
        old_file = Image.objects.get(pk=instance.pk).image
    except Image.DoesNotExist:
        return False
    if old_file != instance.image:
        if os.path.isfile(old_file.path):
            delete_image_and_cache(old_file)


class ImageTag(models.Model):
    """Модель для связи изображений с тегами M2M"""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
