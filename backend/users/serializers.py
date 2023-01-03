import re

from django.contrib.auth import password_validation as pass_val
from recipes.serializers import RecipePartialSerializer
from rest_framework import serializers

from .models import Subscription, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для получения пользователей."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, subscribe):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(
                user=user,
                subscribe=subscribe
            ).exists()
        return False


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователей с валидацией."""
    password = serializers.CharField(
        style={'input_type': 'password'},
        label='Пароль',
        write_only=True
    )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя!'
            )
        if not re.match(r'^[\w.@+-]+\Z', username, flags=re.ASCII):
            raise serializers.ValidationError(
                ('Имя пользователя может содержать латиницу, '
                 'цифры и знаки @ / . / + / - / _')
            )
        elif len(username) < 4:
            raise serializers.ValidationError(
                'Логин должен содержать более 3 символов!'
            )
        return username

    def validate_first_name(self, first_name):
        if not first_name.istitle():
            raise serializers.ValidationError(
                'Имя должно начинаться с заглавной буквы!'
            )
        elif len(first_name) < 2:
            raise serializers.ValidationError(
                'Имя должно содержать от 2 символов!'
            )
        return first_name

    def validate_last_name(self, last_name):
        if not last_name.istitle():
            raise serializers.ValidationError(
                'Фамилия должна начинаться с заглавной буквы!'
            )
        return last_name

    def validate_password(self, password):
        password_validators = pass_val.get_default_password_validators()
        errors = []
        for validator in password_validators:
            try:
                validator.validate(password)
            except serializers.ValidationError as error:
                errors.append(error)
        if errors:
            raise serializers.ValidationError(errors)
        return password

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра подписок."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipePartialSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'id', 'username', 'first_name',
                            'last_name', 'is_subscribed', 'recipes',
                            'recipes_count')

    def get_is_subscribed(self, subscribe):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(
                user=user,
                subscribe=subscribe
            ).exists()
        return False

    def get_recipes_count(self, subscribe):
        return subscribe.recipes.count()
