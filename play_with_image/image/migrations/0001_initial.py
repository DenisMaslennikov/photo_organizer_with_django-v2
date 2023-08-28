# Generated by Django 4.2.1 on 2023-07-10 11:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tag_anything", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="img/%Y/%m/%d", verbose_name="Изображение"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Загружено"
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Обновлено"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Название"),
                ),
                (
                    "image_hash",
                    models.CharField(
                        editable=False,
                        max_length=16,
                        null=True,
                        verbose_name="Хеш изображения",
                    ),
                ),
                (
                    "image_hash_part1",
                    models.IntegerField(
                        editable=False, null=True, verbose_name="Хеш 1/4"
                    ),
                ),
                (
                    "image_hash_part2",
                    models.IntegerField(
                        editable=False, null=True, verbose_name="Хеш 2/4"
                    ),
                ),
                (
                    "image_hash_part3",
                    models.IntegerField(
                        editable=False, null=True, verbose_name="Хеш 3/4"
                    ),
                ),
                (
                    "image_hash_part4",
                    models.IntegerField(
                        editable=False, null=True, verbose_name="Хеш 4/4"
                    ),
                ),
                (
                    "private",
                    models.BooleanField(
                        default=False, verbose_name="Приватное"
                    ),
                ),
                (
                    "camera_model",
                    models.CharField(
                        editable=False,
                        max_length=255,
                        null=True,
                        verbose_name="Камера",
                    ),
                ),
                (
                    "lens_model",
                    models.CharField(
                        editable=False,
                        max_length=255,
                        null=True,
                        verbose_name="Объектив",
                    ),
                ),
                (
                    "iso",
                    models.PositiveIntegerField(
                        editable=False, null=True, verbose_name="ISO"
                    ),
                ),
                (
                    "focal_length",
                    models.FloatField(
                        editable=False,
                        null=True,
                        verbose_name="Фокусное Расстояние",
                    ),
                ),
                (
                    "flash",
                    models.BooleanField(
                        editable=False, null=True, verbose_name="Вспышка"
                    ),
                ),
                (
                    "f",
                    models.FloatField(
                        editable=False, null=True, verbose_name="Диафрагма"
                    ),
                ),
                (
                    "exposure_time",
                    models.CharField(
                        editable=False,
                        max_length=10,
                        null=True,
                        verbose_name="Время Экспозиции",
                    ),
                ),
                (
                    "longitude",
                    models.CharField(
                        editable=False,
                        max_length=11,
                        null=True,
                        verbose_name="Долгота",
                    ),
                ),
                (
                    "latitude",
                    models.CharField(
                        editable=False,
                        max_length=11,
                        null=True,
                        verbose_name="Широта",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
            ],
            options={
                "verbose_name": "изображение",
                "verbose_name_plural": "Изображения",
                "ordering": ("-created",),
                "default_related_name": "images",
            },
        ),
        migrations.CreateModel(
            name="ImageTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="image.image",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tag_anything.tag",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="image",
            name="tags",
            field=models.ManyToManyField(
                through="image.ImageTag",
                to="tag_anything.tag",
                verbose_name="Теги",
            ),
        ),
    ]
