from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(verbose_name='Email', blank=True, unique=True)
    is_active = models.BooleanField(default=True, verbose_name="Is active")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated at")
    is_deleted = models.BooleanField(default=False, verbose_name="Is deleted")

    def __str__(self):
        return f'{self.pk} - {self.username} ({self.email})'

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-username",)
