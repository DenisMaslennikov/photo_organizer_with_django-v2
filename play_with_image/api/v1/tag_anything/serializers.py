from rest_framework import serializers

from tag_anything.models import Tag, TagCategory


class TagCategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий тегов для сериализации в представлении"""
    class Meta:
        model = TagCategory
        fields = '__all__'


class ForTagTagCategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий тегов для сериализации в сериализаторе тегов"""
    class Meta:
        model = TagCategory
        fields = ('id', 'name', 'slug')
        read_only_fields = ('slug',)
        extra_kwargs = {
            'name': {
                'validators': []
            }
        }


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""
    category = ForTagTagCategorySerializer(read_only=False, required=True)

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('created', 'modified')

    def validate_category(self, value):
        try:
            TagCategory.objects.get(name=value.get('name'))
        except TagCategory.DoesNotExist:
            raise serializers.ValidationError(
                'Указана несуществующая категория'
            )
        return value

    def create(self, validated_data):
        category = validated_data.pop('category')
        category = TagCategory.objects.get(name=category.get('name'))
        tag = Tag.objects.create(
            **validated_data,
            category=category
        )
        return tag
