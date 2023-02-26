from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(verbose_name='Email', blank=True, unique=True)

    def __str__(self):
        return f'{self.pk} - {self.last_name} - {self.first_name}'
