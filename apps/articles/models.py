from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.utils.text import slugify
import markdown
import bleach
import uuid

# 尝试导入 PostgreSQL 搜索功能（可选）
import os

_use_postgres = os.environ.get('DB_ENGINE', 'sqlite') == 'postgresql'

if _use_postgres:
    try:
        from django.contrib.postgres.search import SearchVectorField, SearchVector
        HAS_POSTGRES_SEARCH = True
    except ImportError:
        HAS_POSTGRES_SEARCH = False
        _use_postgres = False

if not _use_postgres:
    HAS_POSTGRES_SEARCH = False
    class SearchVectorField(models.TextField):
        def __init__(self, *args, **kwargs):
            kwargs['null'] = True
            kwargs['blank'] = True
            super().__init__(*args, **kwargs)

        def check(self, **kwargs):
            return []


class Category(models.Model):
    """文章分类"""
    name = models.CharField('名称', max_length=50, unique=True)
    slug = models.SlugField('slug', max_length=50, unique=True, blank=True)
    description = models.TextField('描述', blank=True)
    icon = models.CharField('图标', max_length=10, default='📁')
    color = models.CharField('颜色', max_length=20, default='#3B82F6')
    order = models.PositiveIntegerField('排序', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) or f'category-{uuid.uuid4().hex[:8]}'
        super().save(*args, **kwargs)


class Tag(models.Model):
    """文章标签"""
    name = models.CharField('名称', max_length=30, unique=True)
    slug = models.SlugField('slug', max_length=30, unique=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) or f'tag-{uuid.uuid4().hex[:8]}'
        super().save(*args, **kwargs)


class Series(models.Model):
    """专题（文章系列）"""
    title = models.CharField('标题', max_length=100)
    slug = models.SlugField('slug', max_length=100, unique=True, blank=True)
    description = models.TextField('描述', blank=True)
    cover = models.CharField('封面', max_length=500, blank=True, null=True)  # 改为 CharField 存储 URL
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '专题'
        verbose_name_plural = '专题'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}" if base_slug else f'series-{uuid.uuid4().hex[:8]}'
        super().save(*args, **kwargs)


class Article(models.Model):
    """文章模型（支持匿名发布）"""
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )

    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('slug', max_length=200, unique=True, blank=True)
    author = models.ForeignKey(
        User, verbose_name='作者', related_name='articles',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    nickname = models.CharField('昵称', max_length=50, default='匿名用户')
    category = models.ForeignKey(
        Category, verbose_name='分类', related_name='articles',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, verbose_name='标签', related_name='articles', blank=True)
    series = models.ForeignKey(
        Series, verbose_name='专题', related_name='articles',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    content = models.TextField('Markdown内容')
    content_html = models.TextField('HTML内容', blank=True, editable=False)
    summary = models.TextField('摘要', blank=True)
    cover = models.ImageField('封面图片', upload_to='article_covers/%Y/%m/', blank=True, null=True)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='draft')
    is_top = models.BooleanField('置顶', default=False)
    views = models.PositiveIntegerField('阅读量', default=0)
    search_vector = SearchVectorField('搜索向量', null=True, blank=True)  # PostgreSQL 全文搜索
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 自动生成 slug
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
            self.slug = unique_slug
        
        # Markdown 渲染 + XSS 防护
        if self.content:
            html_content = markdown.markdown(
                self.content,
                extensions=['extra', 'codehilite', 'toc']
            )
            # 使用 bleach 清理 HTML，防止 XSS
            allowed_tags = [
                'p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'strong', 'em', 'code', 'pre', 'blockquote',
                'ul', 'ol', 'li', 'a', 'img', 'table', 'thead',
                'tbody', 'tr', 'th', 'td', 'hr'
            ]
            allowed_attrs = {
                'a': ['href', 'title', 'target'],
                'img': ['src', 'alt', 'title'],
                'code': ['class'],
                'pre': ['class'],
            }
            self.content_html = bleach.clean(
                html_content,
                tags=allowed_tags,
                attributes=allowed_attrs,
                strip=True
            )

        # 自动生成摘要（前 200 个字符）
        if not self.summary and self.content:
            # 去除 Markdown 标记
            text_content = bleach.clean(self.content, strip=True)
            self.summary = text_content[:200] + '...' if len(text_content) > 200 else text_content

        super().save(*args, **kwargs)
        
        # 更新搜索向量（仅在使用 PostgreSQL 时）
        self.update_search_vector()
        
        # 尝试更新Elasticsearch索引
        try:
            from .documents import ArticleDocument
            # 这里我们只是确保文档会被更新，django-elasticsearch-dsl会自动处理
        except ImportError:
            # 如果没有安装elasticsearch-dsl，则跳过
            pass
        except Exception as e:
            # Elasticsearch连接错误，忽略
            print(f"⚠ Elasticsearch连接错误: {e}")
    
    def update_search_vector(self):
        """更新全文搜索向量（PostgreSQL）"""
        if not HAS_POSTGRES_SEARCH:
            return
        
        try:
            from django.db import connection
            if connection.vendor == 'postgresql':
                Article.objects.filter(pk=self.pk).update(
                    search_vector=SearchVector('title', weight='A') + 
                                   SearchVector('summary', weight='B') +
                                   SearchVector('content', weight='C')
                )
        except Exception:
            # 如果使用 SQLite 或其他数据库，忽略此功能
            pass

    def increase_views(self):
        """原子递增阅读量（防并发）"""
        Article.objects.filter(pk=self.pk).update(views=F('views') + 1)
        self.refresh_from_db()

    def get_summary(self):
        """获取摘要"""
        return self.summary