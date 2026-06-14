from django.contrib.auth import get_user_model
from rest_framework import serializers

from access.models import Role
from authentication.exceptions import InvalidCredentials

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'role', 'first_name', 'last_name', 'middle_name')
        read_only_fields = ('email',)


class RegistrationSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(many=False, read_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password2': 'Пароли не совпадают'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = User.objects.create_user(password=password, **validated_data)

        default_role = Role.objects.filter(title='user').first()
        if default_role is not None:
            user.role = default_role
            user.save(update_fields=['role'])

        return user

    class Meta:
        model = User
        fields = ('email', 'role', 'first_name', 'last_name', 'middle_name',
                  'password', 'password2')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if (not user or
                not user.check_password(data['password']) or
                not user.is_active):
            raise InvalidCredentials()
        data['user'] = user
        return data
