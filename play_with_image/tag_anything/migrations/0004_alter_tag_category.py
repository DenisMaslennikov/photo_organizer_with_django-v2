# Generated by Django 4.2.1 on 2023-06-23 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tag_anything', '0003_alter_tag_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tag_anything.tagcategory', verbose_name='Категория'),
            preserve_default=False,
        ),
    ]
