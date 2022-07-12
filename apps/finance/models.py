from django.db import models

# Create your models here.
from apps.core.models import User
from apps.utils.abstract_uuid import AbstractUUID
from apps.utils.enums import StatusEnum


class Sales(AbstractUUID):
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    location = models.TextField(default='')
    amount = models.FloatField(default=0.0)
    volume_dispensed = models.PositiveBigIntegerField(default=0)
    status = models.CharField(max_length=20, choices=StatusEnum.choices(), default=StatusEnum.NOT_DONE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.customer_name} {self.amount}'

    class Meta:
        db_table = 'sales'
        verbose_name = 'Sales'
        verbose_name_plural = 'Sales Management'
