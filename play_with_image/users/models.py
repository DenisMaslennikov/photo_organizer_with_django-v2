from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"
