# Generated by Django 4.2.1 on 2023-10-25 06:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tag_anything", "0001_initial"),
        ("image", "0002_alter_image_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="tags",
            field=models.ManyToManyField(
                null=True,
                through="image.ImageTag",
                to="tag_anything.tag",
                verbose_name="Теги",
            ),
        ),
    ]