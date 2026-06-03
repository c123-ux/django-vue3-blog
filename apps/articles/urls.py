from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView
)
from .search_views import ArticleElasticsearchSearchView
from .views_upload import ImageUploadView
from .archive_views import (
    ArticleArchiveView,
    ArticleStatisticsView,
    ArticleArchiveByYearView,
    ArticleArchiveByMonthView
)
from .taxonomy_views import (
    CategoryListView,
    TagListView,
    SeriesListView,
    SeriesDetailView,
    CategoryArticlesView,
    TagArticlesView,
)
from .feeds import LatestArticlesFeed

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    path('search/', ArticleElasticsearchSearchView.as_view(), name='article-search'),
    path('upload-image/', ImageUploadView.as_view(), name='image-upload'),
    # 分类、标签、专题
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/articles/', CategoryArticlesView.as_view(), name='category-articles'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<slug:slug>/articles/', TagArticlesView.as_view(), name='tag-articles'),
    path('series/', SeriesListView.as_view(), name='series-list'),
    path('series/<slug:slug>/', SeriesDetailView.as_view(), name='series-detail'),
    # 归档和统计相关路由
    path('archive/', ArticleArchiveView.as_view(), name='article-archive'),
    path('statistics/', ArticleStatisticsView.as_view(), name='article-statistics'),
    path('archive/<int:year>/', ArticleArchiveByYearView.as_view(), name='article-archive-year'),
    path('archive/<int:year>/<int:month>/', ArticleArchiveByMonthView.as_view(), name='article-archive-month'),
    # RSS 订阅
    path('rss/', LatestArticlesFeed(), name='article-rss'),
]