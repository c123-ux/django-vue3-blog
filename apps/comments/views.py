from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.cache import cache

from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from .throttles import CommentRateThrottle


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return Comment.objects.filter(
            article_id=article_id,
            is_approved=True,
            parent=None
        ).select_related('author').prefetch_related(
            'replies__author'
        ).order_by('-created_at')


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [AllowAny]
    throttle_classes = [CommentRateThrottle]

    def perform_create(self, serializer):
        comment = serializer.save()
        cache.delete(f'article_detail:{comment.article.id}')


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        article_id = instance.article.id
        self.perform_destroy(instance)
        cache.delete(f'article_detail:{article_id}')
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
