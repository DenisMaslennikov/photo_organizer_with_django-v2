import os
from json import loads as read_json, JSONDecodeError

from django.db import transaction, IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from image.models import Image
from api.v1.tag_anything.serializers import TagSerializer


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображений"""
    author = serializers.StringRelatedField()
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Image
        exclude = (
            "image_hash_part1",
            "image_hash_part2",
            "image_hash_part3",
            "image_hash_part4",
        )
        read_only_fields = ('created', 'modified', 'author')

    def create(self, validated_data):
        tags = self.initial_data.get('tags')
        if isinstance(tags, str):
            try:
                tags = read_json(tags)
            except JSONDecodeError:
                raise ParseError('Не удалось декодировать список тегов')
        try:
            with transaction.atomic():
                image = Image.objects.create(**validated_data)
                if tags:
                    image.tags.add(*tags, through_defaults={})
        except IntegrityError:
            if image.image:
                if os.path.isfile(image.image.path):
                    os.remove(image.image.path)
            raise ParseError('Недопустимы ID тега')
        return image


class ImageTagSerializer(serializers.Serializer):
    """Сериализатор для списка id изображений/тегов"""
    tags = serializers.ListField(child=serializers.IntegerField())
    images = serializers.ListField(child=serializers.IntegerField())

    def to_internal_value(self, data):
        images = data.get('images')
        tags = data.get('tags')
        if not images:
            raise serializers.ValidationError(
                {'images': 'Это обязательный параметр'}
            )
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Это обязательный параметр'}
            )
        if not isinstance(images, (list, tuple)):
            raise serializers.ValidationError(
                {'images': 'Должно быть списком'}
            )
        if not isinstance(tags, (list, tuple)):
            raise serializers.ValidationError(
                {'tags': 'Должно быть списком'}
            )
        for image in images:
            if not isinstance(image, int):
                raise serializers.ValidationError(
                    {'images': f'параметр "{image}" должен быть числом'}
                )
        for tag in tags:
            if not isinstance(tag, int):
                raise serializers.ValidationError(
                    {'tags': f'параметр "{tag}" должен быть числом'}
                )
        ret = {
            'tags': tags,
            'images': images,
        }
        return ret
