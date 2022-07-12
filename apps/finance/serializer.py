from datetime import datetime

import pytz
from django.conf import settings
from django.utils.timezone import make_aware
from rest_framework import serializers

from apps.core.models import User
from apps.finance.models import Sales
from apps.utils.enums import StatusEnum


class SalesSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT, read_only=True)
    updated_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT, read_only=True)

    class Meta:
        model = Sales
        fields = '__all__'


class SalesFormSerializer(serializers.Serializer):
    customer_name = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)
    location = serializers.CharField(required=True)
    volume_dispensed = serializers.IntegerField(required=True)
    status = serializers.ChoiceField(choices=StatusEnum.choices())

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            instance.__setattr__(key, value)
        instance.__setattr__('updated_at', make_aware(datetime.today(), timezone=pytz.timezone('Africa/Lagos')))
        instance.save()
        return instance

    def create(self, validated_data):
        instance = Sales.objects.create(**validated_data)
        return instance
