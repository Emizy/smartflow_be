from rest_framework import serializers

from apps.core.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    This class handles serializer handles serializing of user model
    """

    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class UserRegisterSerializer(serializers.Serializer):
    """
    this class handles user registration validation ,creation and update
    """
    name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({'email': 'Email already exist inside our system'})
        return attrs

    def create(self, validated_data):
        instance = User.objects.create(**validated_data)
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance
