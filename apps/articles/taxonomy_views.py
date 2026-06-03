from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Category, Tag, Series, Article
from .serializers import (
    CategorySerializer,
    TagSerializer,
    SeriesListSerializer,
    SeriesDetailSerializer,
    ArticleListSerializer,
)


class CategoryListView(generics.ListAPIView):
    """分类列表（含文章数量）"""
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Category.objects.annotate(
            article_count=Count('articles', distinct=True)
        ).order_by('order', 'name')


class TagListView(generics.ListAPIView):
    """标签列表（含文章数量）"""
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Tag.objects.annotate(
            article_count=Count('articles', distinct=True)
        ).order_by('-article_count', 'name')


class SeriesListView(generics.ListAPIView):
    """专题列表"""
    serializer_class = SeriesListSerializer
    permission_classes = [AllowAny]
    queryset = Series.objects.annotate(
        article_count=Count('articles', distinct=True)
    ).order_by('-created_at')


class SeriesDetailView(generics.RetrieveAPIView):
    """专题详情（含文章列表）"""
    serializer_class = SeriesDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    queryset = Series.objects.annotate(
        article_count=Count('articles', distinct=True)
    )


class CategoryArticlesView(generics.ListAPIView):
    """按分类获取文章"""
    serializer_class = ArticleListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Article.objects.filter(
            status='published',
            category__slug=slug
        ).select_related('author', 'category').prefetch_related('tags')


class TagArticlesView(generics.ListAPIView):
    """按标签获取文章"""
    serializer_class = ArticleListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Article.objects.filter(
            status='published',
            tags__slug=slug
        ).select_related('author', 'category').prefetch_related('tags').distinct()
