from django.contrib.sitemaps import Sitemap
from apps.articles.models import Article, Category, Tag


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Article.objects.filter(status='published').order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/article/{obj.id}'


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        latest = obj.articles.filter(status='published').order_by('-updated_at').first()
        return latest.updated_at if latest else None

    def location(self, obj):
        return f'/categories/{obj.slug}'


class TagSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Tag.objects.all()

    def lastmod(self, obj):
        latest = obj.articles.filter(status='published').order_by('-updated_at').first()
        return latest.updated_at if latest else None

    def location(self, obj):
        return f'/tags/{obj.slug}'
