from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import CommentSerializer
from image.models import Image
from api.v1.core.permissions import IsAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    """API для комментариев"""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        image = get_object_or_404(Image, pk=self.kwargs.get('image_id'))
        return image.comments.all()
