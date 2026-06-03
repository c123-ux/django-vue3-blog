from django.core.cache import cache
from django.db.models import Count, Q
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .models import Article, HAS_POSTGRES_SEARCH
from .permissions import IsAuthorOrStaff
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    ArticleCreateSerializer
)


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'summary']
    ordering_fields = ['created_at', 'views']
    ordering = ['-is_top', '-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'author', 'category'
        ).prefetch_related('tags').defer('content').annotate(
            comments_count=Count('comments', distinct=True)
        )

        search_query = self.request.query_params.get('search', None)
        category = self.request.query_params.get('category', None)
        tag = self.request.query_params.get('tag', None)
        series = self.request.query_params.get('series', None)
        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)

        if category:
            queryset = queryset.filter(category__slug=category)
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        if series:
            queryset = queryset.filter(series__slug=series)
        if year:
            queryset = queryset.filter(created_at__year=year)
        if month:
            queryset = queryset.filter(created_at__month=month)

        if HAS_POSTGRES_SEARCH and search_query:
            try:
                from django.db import connection
                from django.contrib.postgres.search import SearchQuery, SearchRank
                if connection.vendor == 'postgresql':
                    search_vector = 'search_vector'
                    query = SearchQuery(search_query)
                    queryset = queryset.annotate(
                        rank=SearchRank(search_vector, query)
                    ).filter(
                        search_vector=query
                    ).order_by('-rank')
            except Exception:
                pass
        return queryset

    def list(self, request, *args, **kwargs):
        cache_key = f'article_list:{request.query_params}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 300)
        return response


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.filter(status='published').select_related(
        'author', 'category', 'series'
    ).prefetch_related('tags')
    serializer_class = ArticleDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increase_views()

        cache_key = f'article_detail:{instance.id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            cached_data['views'] = instance.views
            return Response(cached_data)

        serializer = self.get_serializer(instance)
        data = serializer.data

        related = self.get_related_articles(instance)
        data['related_articles'] = related

        cache.set(cache_key, data, 600)
        return Response(data)

    def get_related_articles(self, article, limit=4):
        related_qs = Article.objects.filter(status='published').exclude(id=article.id)

        if article.category_id:
            related_qs = related_qs.filter(
                Q(category_id=article.category_id) |
                Q(tags__in=article.tags.all())
            ).distinct()
        else:
            related_qs = related_qs.filter(tags__in=article.tags.all()).distinct()

        if related_qs.count() < limit:
            related_qs = Article.objects.filter(
                status='published'
            ).exclude(id=article.id).order_by('-views')

        related = related_qs[:limit]

        return [
            {
                'id': a.id, 'title': a.title, 'slug': a.slug,
                'summary': a.summary, 'views': a.views, 'created_at': a.created_at
            }
            for a in related
        ]


class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = []  # 允许任何人发布文章，包括匿名用户

    def perform_create(self, serializer):
        # 清除缓存
        cache.delete_pattern('article_list:*')
        serializer.save()


class ArticleUpdateView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrStaff]

    def perform_update(self, serializer):
        instance = self.get_object()
        cache.delete(f'article_detail:{instance.id}')
        serializer.save()


class ArticleDeleteView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrStaff]

    def perform_destroy(self, instance):
        cache.delete(f'article_detail:{instance.id}')
        instance.delete()
