import secrets
from django.db import models


class MonitorServer(models.Model):
    """被监控的服务器"""
    name = models.CharField('名称', max_length=100)
    hostname = models.CharField('主机名', max_length=200, blank=True)
    description = models.TextField('描述', blank=True)
    token = models.CharField('上报令牌', max_length=64, unique=True, editable=False)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '监控服务器'
        verbose_name_plural = '监控服务器'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(32)
        super().save(*args, **kwargs)


class MonitorMetric(models.Model):
    """服务器监控指标上报记录"""
    server = models.ForeignKey(MonitorServer, related_name='metrics', on_delete=models.CASCADE)
    cpu_percent = models.FloatField('CPU使用率')
    memory_percent = models.FloatField('内存使用率')
    disk_percent = models.FloatField('磁盘使用率')
    load_avg = models.FloatField('负载', default=0)
    network_in = models.BigIntegerField('入网流量(bytes)', default=0)
    network_out = models.BigIntegerField('出网流量(bytes)', default=0)
    uptime = models.BigIntegerField('运行时间(秒)', default=0)
    reported_at = models.DateTimeField('上报时间', auto_now_add=True)

    class Meta:
        ordering = ['-reported_at']
        verbose_name = '监控指标'
        verbose_name_plural = '监控指标'
        indexes = [
            models.Index(fields=['server', '-reported_at']),
        ]

    def __str__(self):
        return f'{self.server.name} @ {self.reported_at}'
