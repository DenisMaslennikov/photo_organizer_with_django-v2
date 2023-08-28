from django.db import transaction, IntegrityError
from django.db.models import Q
from django_filters import rest_framework as filters

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import exceptions
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from api.v1.core.exceptions import DoesNotExist, NotAuthorError
from api.v1.image.serializers import ImageSerializer, ImageTagSerializer
from api.v1.core.permissions import IsImageAuthorOrReadOnly
from image.models import Image


class ImageFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author__username')
    camera = filters.CharFilter(field_name='camera_model')
    lens = filters.CharFilter(field_name='lens_model')


class ImageViewSet(ModelViewSet):
    """Апи для работы с изображениями"""

    serializer_class = ImageSerializer
    permission_class = (IsImageAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ImageFilter

    def get_queryset(self):
        """Кверисет с фильтрами по тегам"""
        # Авторизованный пользователь может видеть свои приватные изображения
        if self.request.user.is_authenticated:
            qs = Image.objects.select_related(
                'author').prefetch_related("tags").filter(
                Q(author=self.request.user) | Q(private=False)
            )
        else:
            qs = Image.objects.select_related(
                'author').prefetch_related("tags").filter(private=False)
        # Фильтруем кверисет по набору тегов, если они переданы
        tags = self.request.query_params.get("tags")
        if tags is not None:
            tags = tags.split(",")
            for tag in tags:
                if tag.isdigit():
                    qs = qs & qs.filter(tags=tag)
                else:
                    raise exceptions.ParseError(
                        "tags должно быть числом или набором чисел"
                    )
        return qs

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise exceptions.NotAuthenticated()
        serializer.save(author=self.request.user)

    @extend_schema(parameters=[OpenApiParameter(
        name='tag',
        type=int,
        required=False,
        description=(
            'Фильтр по тегам. Можно указывать несколько через запятую.'
        )
    )])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(url_path='me', detail=False, permission_classes=(IsAuthenticated,))
    def get_my_images(self, request: Request):
        """Просмотр собственных изображений"""
        qs = self.filter_queryset(
            self.get_queryset()).filter(author=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(
        url_path="assign-tags-id-to-images",
        methods=["post"],
        detail=False,
        serializer_class=ImageTagSerializer,
    )
    def assign_tags_id_to_images(self, request: Request):
        """Добавление тегов списку изображений по списку id тегов"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            images = serializer.validated_data.get("images")
            tags = serializer.validated_data.get("tags")
            try:
                with transaction.atomic():
                    for image in Image.objects.filter(id__in=images):
                        if image.author == request.user:
                            image.tags.add(*tags, through_defaults={})
                        else:
                            raise NotAuthorError(
                                f"Вы не владелец изображения {image}"
                            )

            except Image.DoesNotExist:
                raise DoesNotExist("Передан несуществующий ID изображения")
            except IntegrityError:
                raise DoesNotExist("Передан несуществующий ID тега")
            changed_images = Image.objects.filter(id__in=images)
            serializer = ImageSerializer(changed_images, many=True)
            return Response(serializer.data)
        return Response(serializer.errors)

    @action(
        url_path="remove-tags-id-from-images",
        methods=["post"],
        detail=False,
        serializer_class=ImageTagSerializer,
    )
    def remove_tags_id_from_images(self, request: Request):
        """Удаление тегов у списка изображений по списку id тегов"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            images = serializer.validated_data.get("images")
            tags = serializer.validated_data.get("tags")
            try:
                with transaction.atomic():
                    for image in Image.objects.filter(id__in=images):
                        if image.author == request.user:
                            image.tags.remove(*tags)
                        else:
                            raise NotAuthorError(
                                f"Вы не владелец изображения {image}"
                            )
            except Image.DoesNotExist:
                raise DoesNotExist("Передан несуществующий ID изображения")
            changed_images = Image.objects.filter(id__in=images)
            serializer = ImageSerializer(changed_images, many=True)
            return Response(serializer.data)
        return Response(serializer.errors)
