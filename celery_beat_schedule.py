from celery.schedules import crontab

# Celery Beat调度配置
# 用于定期执行定时任务

CELERY_BEAT_SCHEDULE = {
    # 每天凌晨2点执行文章统计
    'update-article-statistics': {
        'task': 'apps.articles.tasks.update_article_statistics',
        'schedule': crontab(hour=2, minute=0),  # 每天凌晨2点
    },
    
    # 每小时执行缓存清理
    'cleanup-old-cache': {
        'task': 'apps.articles.tasks.cleanup_old_cache',
        'schedule': crontab(minute=0),  # 每小时整点
    },
    
    # 每天早上8点生成日报
    'generate-daily-report': {
        'task': 'apps.articles.tasks.generate_daily_report',
        'schedule': crontab(hour=8, minute=0),  # 每天早上8点
    },
    
    # 每天晚上11点清理临时文件
    'cleanup-temp-files': {
        'task': 'apps.articles.tasks.cleanup_temp_files',
        'schedule': crontab(hour=23, minute=0),  # 每天晚上11点
    },
}

# 添加到settings.py中的CELERY配置
CELERY_BEAT_SCHEDULE