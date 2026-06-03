from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.articles.models import Article


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Article.objects.filter(status='published').order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/article/{obj.id}'


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home', 'categories', 'archive', 'notes', 'tools', 'about']

    def location(self, item):
        paths = {
            'home': '/',
            'categories': '/categories',
            'archive': '/archive',
            'notes': '/notes',
            'tools': '/tools',
            'about': '/about',
        }
        return paths.get(item, '/')
