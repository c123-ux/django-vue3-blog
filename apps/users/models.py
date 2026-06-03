from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """用户扩展资料"""
    user = models.OneToOneField(
        User, verbose_name='用户', related_name='profile', on_delete=models.CASCADE
    )
    avatar = models.ImageField('头像', upload_to='avatars/%Y/%m/', blank=True, null=True)
    bio = models.TextField('个人简介', blank=True, max_length=500)
    website = models.URLField('个人网站', blank=True)
    github = models.URLField('GitHub', blank=True)
    location = models.CharField('所在地', max_length=100, blank=True)

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f'{self.user.username} 的资料'


class SocialAccount(models.Model):
    """第三方 OAuth 账号绑定"""
    PROVIDER_CHOICES = (
        ('github', 'GitHub'),
        ('wechat', '微信'),
    )
    user = models.ForeignKey(User, related_name='social_accounts', on_delete=models.CASCADE)
    provider = models.CharField('提供商', max_length=20, choices=PROVIDER_CHOICES)
    uid = models.CharField('第三方用户ID', max_length=100)
    extra_data = models.JSONField('扩展数据', default=dict, blank=True)
    created_at = models.DateTimeField('绑定时间', auto_now_add=True)

    class Meta:
        verbose_name = '社交账号'
        verbose_name_plural = '社交账号'
        unique_together = [('provider', 'uid')]

    def __str__(self):
        return f'{self.user.username} - {self.provider}'
