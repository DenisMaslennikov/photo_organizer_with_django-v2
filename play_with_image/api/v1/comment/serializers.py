from rest_framework import serializers

from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Серриалайзер комментариев"""
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('author',)
