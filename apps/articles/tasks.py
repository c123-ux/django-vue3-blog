from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_article_notification_email(user_email, article_title, article_url):
    """
    异步发送文章发布通知邮件
    """
    try:
        subject = f'新文章发布：{article_title}'
        
        html_message = render_to_string('emails/article_notification.html', {
            'article_title': article_title,
            'article_url': article_url,
        })
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f'邮件发送成功：{user_email}')
        return {'status': 'success', 'email': user_email}
        
    except Exception as e:
        logger.error(f'邮件发送失败：{user_email}, 错误：{str(e)}')
        return {'status': 'error', 'email': user_email, 'error': str(e)}


@shared_task
def send_comment_notification_email(author_email, commenter_username, article_title, comment_content):
    """
    异步发送评论通知邮件
    """
    try:
        subject = f'您的文章收到新评论：{article_title}'
        
        html_message = render_to_string('emails/comment_notification.html', {
            'commenter_username': commenter_username,
            'article_title': article_title,
            'comment_content': comment_content,
        })
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[author_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f'评论通知邮件发送成功：{author_email}')
        return {'status': 'success', 'email': author_email}
        
    except Exception as e:
        logger.error(f'评论通知邮件发送失败：{author_email}, 错误：{str(e)}')
        return {'status': 'error', 'email': author_email, 'error': str(e)}


@shared_task
def process_image_upload(image_path):
    """
    异步处理图片上传（压缩、生成缩略图等）
    """
    try:
        from PIL import Image
        import os
        
        img = Image.open(image_path)
        
        # 生成缩略图
        thumbnail_path = image_path.replace('.', '_thumb.')
        img.thumbnail((300, 300))
        img.save(thumbnail_path, 'JPEG', quality=85)
        
        # 压缩原图
        if img.width > 1920 or img.height > 1080:
            img.thumbnail((1920, 1080))
            img.save(image_path, 'JPEG', quality=90)
        
        logger.info(f'图片处理成功：{image_path}')
        return {'status': 'success', 'path': image_path}
        
    except Exception as e:
        logger.error(f'图片处理失败：{image_path}, 错误：{str(e)}')
        return {'status': 'error', 'path': image_path, 'error': str(e)}


@shared_task
def update_article_statistics():
    """
    定时任务：更新文章统计信息
    每天凌晨执行
    """
    try:
        from apps.articles.models import Article
        from django.db.models import Count, Q
        from django.utils import timezone
        from datetime import timedelta
        
        # 统计过去7天的热门文章
        week_ago = timezone.now() - timedelta(days=7)
        popular_articles = Article.objects.filter(
            created_at__gte=week_ago
        ).order_by('-views')[:10]
        
        logger.info(f'热门文章统计完成：{len(popular_articles)} 篇')
        return {'status': 'success', 'count': len(popular_articles)}
        
    except Exception as e:
        logger.error(f'文章统计失败：{str(e)}')
        return {'status': 'error', 'error': str(e)}


@shared_task
def cleanup_old_cache():
    """
    定时任务：清理过期缓存
    每小时执行
    """
    try:
        from django.core.cache import cache
        
        # 这里可以添加特定的缓存清理逻辑
        # 例如清理超过一定时间未访问的缓存
        
        logger.info('缓存清理完成')
        return {'status': 'success'}
        
    except Exception as e:
        logger.error(f'缓存清理失败：{str(e)}')
        return {'status': 'error', 'error': str(e)}


@shared_task
def generate_daily_report():
    """
    定时任务：生成每日报告
    每天凌晨执行
    """
    try:
        from apps.articles.models import Article
        from apps.comments.models import Comment
        from django.contrib.auth.models import User
        from django.utils import timezone
        from datetime import timedelta
        
        yesterday = timezone.now() - timedelta(days=1)
        today = timezone.now()
        
        # 统计数据
        new_articles = Article.objects.filter(
            created_at__range=(yesterday, today)
        ).count()
        
        new_comments = Comment.objects.filter(
            created_at__range=(yesterday, today)
        ).count()
        
        new_users = User.objects.filter(
            date_joined__range=(yesterday, today)
        ).count()
        
        report = {
            'date': yesterday.date().isoformat(),
            'new_articles': new_articles,
            'new_comments': new_comments,
            'new_users': new_users,
        }
        
        logger.info(f'每日报告生成完成：{report}')
        return {'status': 'success', 'report': report}
        
    except Exception as e:
        logger.error(f'每日报告生成失败：{str(e)}')
        return {'status': 'error', 'error': str(e)}


@shared_task
def cleanup_temp_files():
    """
    定时任务：清理临时文件
    每天晚上执行
    """
    try:
        import os
        from django.conf import settings
        from datetime import datetime, timedelta
        
        # 清理临时上传目录中的旧文件
        temp_dir = settings.MEDIA_ROOT / 'temp'
        if temp_dir.exists():
            cutoff_date = datetime.now() - timedelta(days=1)  # 一天前的文件
            
            for filename in temp_dir.iterdir():
                if filename.stat().st_mtime < cutoff_date.timestamp():
                    os.remove(filename)
                    logger.info(f'删除临时文件：{filename}')
        
        logger.info('临时文件清理完成')
        return {'status': 'success'}
        
    except Exception as e:
        logger.error(f'临时文件清理失败：{str(e)}')
        return {'status': 'error', 'error': str(e)}


@shared_task
def send_weekly_digest():
    """
    定时任务：发送周报
    每周一上午发送上周统计数据
    """
    try:
        from apps.articles.models import Article
        from apps.comments.models import Comment
        from django.contrib.auth.models import User
        from django.utils import timezone
        from datetime import timedelta
        
        # 获取上周的数据
        now = timezone.now()
        start_of_last_week = (now - timedelta(days=now.weekday() + 7)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_last_week = (start_of_last_week + timedelta(days=7))
        
        # 统计数据
        last_week_articles = Article.objects.filter(
            created_at__range=(start_of_last_week, end_of_last_week)
        ).count()
        
        last_week_comments = Comment.objects.filter(
            created_at__range=(start_of_last_week, end_of_last_week)
        ).count()
        
        last_week_users = User.objects.filter(
            date_joined__range=(start_of_last_week, end_of_last_week)
        ).count()
        
        # 发送给所有活跃用户
        active_users = User.objects.filter(is_active=True, email__isnull=False)
        
        for user in active_users:
            subject = f'博客周报 - {start_of_last_week.strftime("%m月%d日")} 至 {end_of_last_week.strftime("%m月%d日")}'
            message = f"""
            您好 {user.username},
            
            这是上周的博客统计：
            - 新增文章: {last_week_articles}
            - 新增评论: {last_week_comments}
            - 新增用户: {last_week_users}
            
            感谢您的关注！
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        
        logger.info(f'周报发送完成，共发送给 {active_users.count()} 位用户')
        return {'status': 'success', 'recipients_count': active_users.count()}
        
    except Exception as e:
        logger.error(f'周报发送失败：{str(e)}')
        return {'status': 'error', 'error': str(e)}