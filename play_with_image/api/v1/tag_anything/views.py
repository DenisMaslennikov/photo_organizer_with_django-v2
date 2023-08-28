from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from api.v1.tag_anything.serializers import (
    TagCategorySerializer,
    TagSerializer
)
from api.v1.core.permissions import IsAdminOrReadOnly
from tag_anything.models import Tag, TagCategory


class TagViewSet(ModelViewSet):
    """Управление тегами"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = (IsAuthenticatedOrReadOnly,)


class TagCategoryViewSet(ModelViewSet):
    """Просмотр категорий тегов"""
    queryset = TagCategory.objects.all()
    serializer_class = TagCategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
