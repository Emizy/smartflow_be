import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    USER MODELS
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'user'
        ordering = ('-date_joined',)
        verbose_name_plural = 'User'

    def __str__(self):
        return f"{self.id} {self.username} {self.name}"
