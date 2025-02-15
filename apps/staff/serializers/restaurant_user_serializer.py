from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.models import RestaurantUser


class RestaurantUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = RestaurantUser
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'restaurant',
        ]


class RestaurantUserDetailSerializer(RestaurantUserSerializer):
    permissions = serializers.ListField(read_only=True)
    restaurant_name = serializers.CharField(read_only=True, source='restaurant.name')

    def to_representation(self, instance: RestaurantUser):
        representation = super().to_representation(instance)
        representation['permissions'] = list(instance.get_all_permissions())
        return representation

    class Meta:
        model = RestaurantUser
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'restaurant',
            'restaurant_name',
            'permissions',
        ]


class PasswordSerializer(serializers.Serializer):
    password_one = serializers.CharField()
    password_two = serializers.CharField()

    def validate(self, attrs):
        user = self.context['user']
        password_one = attrs['password_one']
        password_two = attrs['password_two']
        if password_one != password_two:
            raise ValidationError('the passwords to not match')
        validate_password(password_one, user)
        return super().validate(attrs)

    def get_validated_password(self) -> str:
        return self.validated_data['password_one']


class RestaurantUserPermissionSerializer(serializers.Serializer):
    permission_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)
