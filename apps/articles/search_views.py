import os
import logging

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.db.models import Q

logger = logging.getLogger(__name__)

from .models import Article
from .serializers import ArticleListSerializer

USE_ELASTICSEARCH = os.environ.get('USE_ELASTICSEARCH', 'false').lower() == 'true'


def _elasticsearch_search(query, limit=50):
    """Elasticsearch 搜索，失败时返回 None"""
    if not USE_ELASTICSEARCH:
        return None
    try:
        from apps.articles.documents import ArticleDocument
        search = ArticleDocument.search().query(
            'multi_match',
            query=query,
            fields=['title^3', 'summary^2', 'content'],
            type='best_fields',
            fuzziness='AUTO',
        ).filter('term', status='published')[:limit]

        ids = [int(hit.meta.id) for hit in search.execute()]
        if not ids:
            return Article.objects.none(), Article.objects.none()

        preserved = {pk: i for i, pk in enumerate(ids)}
        exact_results = Article.objects.filter(id__in=ids, status='published')
        exact_results = sorted(exact_results, key=lambda x: preserved.get(x.id, 999))

        exact_ids = set(ids)
        related_results = Article.objects.filter(
            status='published', content__icontains=query
        ).exclude(id__in=exact_ids).order_by('-views')[:5]

        return exact_results, related_results
    except Exception as e:
        logger.warning('Elasticsearch search failed, fallback to ORM: %s', e)
        return None


def _orm_search(query):
    exact_results = Article.objects.filter(
        status='published'
    ).filter(
        Q(title__icontains=query) | Q(summary__icontains=query)
    ).order_by('-created_at')

    exact_ids = set(exact_results.values_list('id', flat=True))
    related_results = Article.objects.filter(
        status='published', content__icontains=query
    ).exclude(id__in=exact_ids).order_by('-views', '-created_at')[:5]

    return exact_results, related_results


class ArticleElasticsearchSearchView(generics.ListAPIView):
    """全文搜索（Elasticsearch 优先，ORM 降级）"""
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')

        if not query:
            return Response({'results': [], 'count': 0, 'related': [], 'message': '请输入搜索关键词'})

        try:
            es_result = _elasticsearch_search(query)
            if es_result is not None:
                exact_results, related_results = es_result
                engine = 'elasticsearch'
            else:
                exact_results, related_results = _orm_search(query)
                engine = 'database'

            exact_serializer = self.get_serializer(exact_results, many=True)
            related_serializer = self.get_serializer(related_results, many=True)

            return Response({
                'results': exact_serializer.data,
                'count': len(exact_serializer.data) if engine == 'elasticsearch' else exact_results.count(),
                'related': related_serializer.data,
                'related_count': len(related_serializer.data),
                'search_query': query,
                'engine': engine,
            })
        except Exception as e:
            logger.error('搜索处理失败: %s', e)
            return Response(
                {'error': '搜索服务暂时不可用，请稍后再试'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
