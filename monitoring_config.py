"""
性能监控和指标收集配置
用于Prometheus等监控系统
"""
import os

# 是否启用性能监控
ENABLE_PROMETHEUS_METRICS = os.environ.get('ENABLE_PROMETHEUS_METRICS', 'False').lower() == 'true'

# 如果启用Prometheus监控，需要添加到INSTALLED_APPS
if ENABLE_PROMETHEUS_METRICS:
    PROMETHEUS_MIDDLEWARE = [
        'django_prometheus.middleware.PrometheusBeforeMiddleware',
        'django_prometheus.middleware.PrometheusAfterMiddleware',
    ]
else:
    PROMETHEUS_MIDDLEWARE = []

# 监控指标配置
MONITORING_CONFIG = {
    'enable_db_metrics': True,  # 启用数据库性能指标
    'enable_cache_metrics': True,  # 启用缓存性能指标
    'enable_system_metrics': True,  # 启用系统性能指标
    'metrics_prefix': 'blog_',  # 指标前缀
    'scrape_interval': 30,  # 指标采集间隔（秒）
}