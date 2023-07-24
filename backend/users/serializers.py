from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import Subscriber

User = get_user_model()


class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer creating user instances."""
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password')
        )
        return super(UserCreateSerializer, self).create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Serializer representing user instances."""
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Subscriber.objects.filter(
            user=request.user.id,
            subscriber=obj.id
        ).exists()
