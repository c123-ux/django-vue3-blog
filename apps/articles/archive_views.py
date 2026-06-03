"""
文章归档和统计视图
提供文章按日期归档、统计数据等功能
"""
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth, TruncYear
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.cache import cache

from .models import Article


class ArticleArchiveView(generics.GenericAPIView):
    """
    文章归档视图
    按年份和月份归档文章
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        获取文章归档数据
        返回格式：
        [
            {
                "year": 2024,
                "months": [
                    {
                        "month": 5,
                        "count": 10,
                        "articles": [...]
                    }
                ]
            }
        ]
        """
        # 尝试从缓存获取
        cache_key = 'article_archive'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        # 按年份和月份分组统计文章
        articles = Article.objects.filter(status='published').order_by('-created_at')
        
        # 按年份分组
        years_data = {}
        
        for article in articles:
            year = article.created_at.year
            month = article.created_at.month
            
            if year not in years_data:
                years_data[year] = {
                    'year': year,
                    'months': {}
                }
            
            if month not in years_data[year]['months']:
                years_data[year]['months'][month] = {
                    'month': month,
                    'count': 0,
                    'articles': []
                }
            
            years_data[year]['months'][month]['count'] += 1
            years_data[year]['months'][month]['articles'].append({
                'id': article.id,
                'title': article.title,
                'created_at': article.created_at.isoformat(),
                'views': article.views
            })
        
        # 转换为列表格式
        result = []
        for year_data in sorted(years_data.values(), key=lambda x: x['year'], reverse=True):
            months_list = sorted(year_data['months'].values(), key=lambda x: x['month'], reverse=True)
            year_data['months'] = months_list
            result.append(year_data)
        
        # 写入缓存（1小时）
        cache.set(cache_key, result, 3600)
        
        return Response(result)


class ArticleStatisticsView(generics.GenericAPIView):
    """
    文章统计视图
    提供文章统计数据
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        获取文章统计数据
        返回格式：
        {
            "total_articles": 100,
            "total_views": 10000,
            "average_views": 100,
            "most_viewed": [...],
            "recent_articles": [...],
            "articles_by_category": {...},
            "articles_by_month": [...]
        }
        """
        # 尝试从缓存获取
        cache_key = 'article_statistics'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        articles = Article.objects.filter(status='published')
        
        # 基础统计
        total_articles = articles.count()
        total_views = articles.aggregate(total=Sum('views'))['total'] or 0
        average_views = articles.aggregate(avg=Avg('views'))['avg'] or 0
        
        # 最受欢迎的文章（前10篇）
        most_viewed = articles.order_by('-views')[:10]
        most_viewed_data = [
            {
                'id': article.id,
                'title': article.title,
                'views': article.views,
                'created_at': article.created_at.isoformat()
            }
            for article in most_viewed
        ]
        
        # 最新文章（前10篇）
        recent_articles = articles.order_by('-created_at')[:10]
        recent_articles_data = [
            {
                'id': article.id,
                'title': article.title,
                'views': article.views,
                'created_at': article.created_at.isoformat()
            }
            for article in recent_articles
        ]
        
        # 按分类统计
        articles_by_category = articles.filter(
            category__isnull=False
        ).values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        category_stats = {}
        for item in articles_by_category:
            if item['category__name']:
                category_stats[item['category__name']] = item['count']
        
        # 按月份统计（最近12个月）
        articles_by_month = articles.annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('-month')[:12]
        
        month_stats = [
            {
                'month': item['month'].isoformat(),
                'count': item['count']
            }
            for item in articles_by_month
        ]
        
        # 按年份统计
        articles_by_year = articles.annotate(
            year=TruncYear('created_at')
        ).values('year').annotate(
            count=Count('id')
        ).order_by('-year')
        
        year_stats = [
            {
                'year': item['year'].isoformat(),
                'count': item['count']
            }
            for item in articles_by_year
        ]
        
        result = {
            'total_articles': total_articles,
            'total_views': total_views,
            'average_views': round(average_views, 2),
            'most_viewed': most_viewed_data,
            'recent_articles': recent_articles_data,
            'articles_by_category': category_stats,
            'articles_by_month': month_stats,
            'articles_by_year': year_stats
        }
        
        # 写入缓存（30分钟）
        cache.set(cache_key, result, 1800)
        
        return Response(result)


class ArticleArchiveByYearView(generics.GenericAPIView):
    """
    按年份获取文章归档
    """
    permission_classes = [AllowAny]
    
    def get(self, request, year):
        """
        获取指定年份的文章归档
        """
        cache_key = f'article_archive_year_{year}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        articles = Article.objects.filter(
            status='published',
            created_at__year=year
        ).order_by('-created_at')
        
        # 按月份分组
        months_data = {}
        
        for article in articles:
            month = article.created_at.month
            
            if month not in months_data:
                months_data[month] = {
                    'month': month,
                    'count': 0,
                    'articles': []
                }
            
            months_data[month]['count'] += 1
            months_data[month]['articles'].append({
                'id': article.id,
                'title': article.title,
                'created_at': article.created_at.isoformat(),
                'views': article.views
            })
        
        # 转换为列表格式
        result = sorted(months_data.values(), key=lambda x: x['month'], reverse=True)
        
        # 写入缓存（1小时）
        cache.set(cache_key, result, 3600)
        
        return Response({
            'year': year,
            'total_count': articles.count(),
            'months': result
        })


class ArticleArchiveByMonthView(generics.GenericAPIView):
    """
    按年月获取文章归档
    """
    permission_classes = [AllowAny]
    
    def get(self, request, year, month):
        """
        获取指定年月的文章列表
        """
        cache_key = f'article_archive_{year}_{month}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        articles = Article.objects.filter(
            status='published',
            created_at__year=year,
            created_at__month=month
        ).order_by('-created_at')
        
        result = [
            {
                'id': article.id,
                'title': article.title,
                'summary': article.summary,
                'created_at': article.created_at.isoformat(),
                'views': article.views,
                'author': article.author.username
            }
            for article in articles
        ]
        
        # 写入缓存（1小时）
        cache.set(cache_key, result, 3600)
        
        return Response({
            'year': year,
            'month': month,
            'total_count': len(result),
            'articles': result
        })