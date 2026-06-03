from django.contrib.syndication.views import Feed
from django.urls import reverse

from .models import Article


class LatestArticlesFeed(Feed):
    title = '最新文章'
    link = '/rss/'
    description = '博客最新文章动态'

    def items(self):
        return Article.objects.filter(status='published').order_by('-created_at')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary or item.content[:200]

    def item_link(self, item):
        if item.slug:
            return reverse('article-detail', args=[item.slug])
        return f'/article/{item.id}/'

    def item_pubdate(self, item):
        return item.created_at

    def item_author_name(self, item):
        return item.author.username
