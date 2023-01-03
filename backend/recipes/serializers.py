import base64
import imghdr
import uuid

import six
from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Recipe


class Base64ImageField(serializers.ImageField):
    """Поле для декодирования изображения из base64."""
    def to_representation(self, value):
        return value.url

    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('Загрузите корректное изображение')
            file_name = str(uuid.uuid4())[:12]
            extension = imghdr.what(file_name, decoded_file)
            extension = 'jpg' if extension == 'jpeg' else extension
            complete_file_name = f'{file_name}.{extension}'
            data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)


class RecipePartialSerializer(serializers.ModelSerializer):
    """Сериализатор для получения рецептов в подписчиках."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
