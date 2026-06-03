from datetime import date

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from apps.articles.models import Category, Tag, Article
from apps.system.models import SiteConfig, FriendLink
from apps.users.models import UserProfile
from apps.notes.models import Note
from apps.monitoring.models import MonitorServer


class Command(BaseCommand):
    help = '初始化博客默认数据（分类、标签、站点配置、友情链接）'

    def handle(self, *args, **options):
        categories = [
            {'name': 'Python Web开发', 'slug': 'python-web', 'icon': '🐍', 'color': '#3776AB', 'order': 1},
            {'name': '容器化', 'slug': 'docker', 'icon': '🐳', 'color': '#2496ED', 'order': 2},
            {'name': 'Linux 笔记', 'slug': 'linux', 'icon': '🐧', 'color': '#FCC624', 'order': 3},
            {'name': '数据库&中间件', 'slug': 'database', 'icon': '🗄️', 'color': '#4479A1', 'order': 4},
            {'name': '监控', 'slug': 'monitoring', 'icon': '📊', 'color': '#E6522C', 'order': 5},
            {'name': '工作经验', 'slug': 'work', 'icon': '💼', 'color': '#6366F1', 'order': 6},
            {'name': '前端', 'slug': 'frontend', 'icon': '💚', 'color': '#42B883', 'order': 7},
            {'name': 'CI/CD', 'slug': 'cicd', 'icon': '🔧', 'color': '#EC4899', 'order': 8},
        ]

        for cat_data in categories:
            Category.objects.update_or_create(slug=cat_data['slug'], defaults=cat_data)

        tags = [
            'Django', 'Vue3', 'Python', 'Redis', 'Docker', 'Nginx',
            'Celery', 'PostgreSQL', 'JWT', 'REST API', 'Prometheus', 'GitHub Actions'
        ]
        for tag_name in tags:
            Tag.objects.get_or_create(name=tag_name)

        SiteConfig.objects.update_or_create(
            pk=1,
            defaults={
                'site_name': 'TendCode',
                'site_description': '一个使用 Django + Vue3 搭建的个人技术博客，分享编程学习心得',
                'site_keywords': 'Python,Django,Vue3,博客,技术分享,容器化,监控',
                'author_name': '技术博主',
                'author_bio': '热爱技术，专注于 Python、Django、Vue3 等技术栈',
                'notice': '🎉 欢迎来到我的技术博客！\n📝 这里分享 Python、Django、Vue3 等技术文章\n💡 持续更新中，敬请关注',
                'start_date': date(2018, 1, 1),
                'github_url': 'https://github.com/Hopetree/izone',
            }
        )

        friend_links = [
            {'name': 'izone 博客源码', 'url': 'https://github.com/Hopetree/izone', 'order': 1},
            {'name': 'TendCode 演示站', 'url': 'https://tendcode.com/', 'order': 2},
            {'name': 'Django 官方文档', 'url': 'https://docs.djangoproject.com/', 'order': 3},
            {'name': 'Vue3 官方文档', 'url': 'https://vuejs.org/', 'order': 4},
        ]
        for link_data in friend_links:
            FriendLink.objects.update_or_create(name=link_data['name'], defaults=link_data)

        for user in User.objects.all():
            UserProfile.objects.get_or_create(user=user)

        # 为已有文章自动分配分类和标签
        default_category = Category.objects.filter(slug='python-web').first()
        django_tag = Tag.objects.filter(name='Django').first()
        python_tag = Tag.objects.filter(name='Python').first()

        for article in Article.objects.filter(category__isnull=True):
            if default_category:
                article.category = default_category
                article.save(update_fields=['category'])
            if django_tag:
                article.tags.add(django_tag)
            if python_tag:
                article.tags.add(python_tag)

        admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if admin_user:
            sample_notes = [
                {'title': 'Python 装饰器详解', 'tags': 'Python,装饰器', 'content': '# Python 装饰器详解\n\n装饰器是 Python 中一种强大的语法特性。'},
                {'title': 'Django Redis 缓存配置', 'tags': 'Django,Redis', 'content': '# Django Redis 缓存\n\n配置 Redis 作为缓存后端可以显著提升性能。'},
                {'title': 'Vue3 组合式 API', 'tags': 'Vue3,JavaScript', 'content': '# Vue3 组合式 API\n\n组合式 API 提供更灵活的代码组织方式。'},
            ]
            for note_data in sample_notes:
                Note.objects.get_or_create(
                    title=note_data['title'], author=admin_user,
                    defaults={**note_data, 'is_public': True}
                )

        server, created = MonitorServer.objects.get_or_create(
            name='本地开发服务器',
            defaults={'hostname': 'localhost', 'description': '开发环境监控'}
        )
        if created:
            self.stdout.write(f'  监控令牌: {server.token}')

        self.stdout.write(self.style.SUCCESS(
            f'OK: {Category.objects.count()} categories, '
            f'{Tag.objects.count()} tags, '
            f'{Note.objects.count()} notes, '
            f'{FriendLink.objects.count()} friend links'
        ))
