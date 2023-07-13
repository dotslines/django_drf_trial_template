from typing import Dict

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    The Account model basic serializer.
    """
    class Meta:
        model = Account
        fields = 'id', 'username', 'email', 'first_name', 'password'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self,
               validated_data: Dict[str, str]) -> Account:
        account = Account(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        account.set_password(validated_data['password'])
        account.save()
        return account


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    The Account model serializer for a change password case.
    """
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     validators=(validate_password,))
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = 'password', 'password2', 'old_password'

    def validate_old_password(self,
                              value: str) -> str:
        """
        Validate an old password, check it's correctness.
        """
        account = self.context['request'].user
        if not account.check_password(value):
            raise serializers.ValidationError(
                {'old_password': 'Old password is not correct!'}
            )
        return value

    def validate(self,
                 attrs: Dict[str, str]) -> Dict[str, str]:
        """
        Validate a new password.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match!"}
            )
        return attrs

    def update(self,
               instance: Account,
               validated_data: Dict[str, str]) -> Account:
        """
        Update an account with a new password.
        """
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    """
    The login serializer.
    Not a ModelSerializer.
    """
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self,
                 attrs: Dict[str, str]) -> Dict[str, str]:
        """
        Validates the login fields.
        """
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError(
                    "wrong username or password",
                    code="authorization"
                )
        else:
            raise serializers.ValidationError(
                "username and password are required",
                code="authorization"
            )

        attrs['user'] = user
        return attrs
