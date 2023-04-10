from django.contrib.auth\
    .password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = 'id', 'username', 'email', 'first_name', 'password'
    
    def create(self, validated_data):
        print(validated_data, '*************************')
        account = Account(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        account.set_password(validated_data['password'])
        account.save()
        return account


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     validators=(validate_password,))
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Account
        fields = ('password', 'password2', 'old_password')
    
    def validate_old_password(self, value):
        account = self.context['request'].user
        if not account.check_password(value):
            raise serializers.ValidationError(
                {'old_password': 'Old password is not correct!'}
            )
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match!"}
            )
        return attrs
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
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