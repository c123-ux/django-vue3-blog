"""
URL configuration for blog_backend project.
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse

from apps.articles.sitemaps import ArticleSitemap, CategorySitemap, TagSitemap
from blog_backend.sitemaps import StaticViewSitemap
from blog_backend.seo_views import robots_txt

sitemaps = {
    'articles': ArticleSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap,
    'static': StaticViewSitemap,
}


def api_root(request):
    return JsonResponse({
        'message': '欢迎来到博客系统API',
        'version': '2.0.0',
        'available_endpoints': {
            'admin': '/admin/',
            'health': '/health/',
            'docs': '/api/docs/',
            'sitemap': '/sitemap.xml',
            'robots': '/robots.txt',
            'metrics': '/metrics/',
            'auth': {
                'token': '/api/auth/token/',
                'oauth_github': '/api/auth/oauth/github/',
                'oauth_weibo': '/api/auth/oauth/weibo/',
            },
            'articles': '/api/articles/',
            'notes': '/api/notes/',
            'monitoring': '/api/monitoring/',
            'comments': '/api/comments/',
            'site': '/api/site/',
        },
        'features': [
            'JWT + OAuth(GitHub/微博)',
            '分类/标签/专题/便签',
            '嵌套评论 + WebSocket',
            'Elasticsearch搜索(可降级)',
            'Sitemap/SEO',
            '服务器监控',
            'Prometheus指标',
        ]
    })


urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('health/', include('apps.system.urls')),
    path('api/site/', include('apps.system.site_urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots-txt'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('api/auth/', include('apps.users.urls')),
    path('api/articles/', include('apps.articles.urls')),
    path('api/comments/', include('apps.comments.urls')),
    path('api/notes/', include('apps.notes.urls')),
    path('api/monitoring/', include('apps.monitoring.urls')),
]

if getattr(settings, 'ENABLE_PROMETHEUS_METRICS', True):
    try:
        urlpatterns += [path('', include('django_prometheus.urls'))]
    except ImportError:
        pass

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
