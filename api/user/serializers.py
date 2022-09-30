"""
User related serializers.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        data['email'] = self.user.email
        data['name'] = self.user.name
        data['superuser'] = self.user.is_superuser

        return data


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Creates and returns a user"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Updates a user."""
        password = validated_data.pop('password', )
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
