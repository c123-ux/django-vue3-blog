from django.db import models


class SiteConfig(models.Model):
    """站点配置（单例）"""
    site_name = models.CharField('站点名称', max_length=100, default='TendCode')
    site_description = models.TextField('站点描述', blank=True)
    site_keywords = models.CharField('关键词', max_length=200, blank=True)
    author_name = models.CharField('作者名称', max_length=50, default='技术博主')
    author_bio = models.TextField('作者简介', blank=True)
    author_avatar = models.ImageField('作者头像', upload_to='site/', blank=True, null=True)
    icp_number = models.CharField('ICP备案号', max_length=50, blank=True)
    github_url = models.URLField('GitHub', blank=True)
    notice = models.TextField('网站公告', blank=True)
    start_date = models.DateField('建站日期', null=True, blank=True)

    class Meta:
        verbose_name = '站点配置'
        verbose_name_plural = '站点配置'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class FriendLink(models.Model):
    """友情链接"""
    name = models.CharField('名称', max_length=50)
    url = models.URLField('链接')
    description = models.CharField('描述', max_length=200, blank=True)
    logo = models.ImageField('Logo', upload_to='friend_links/', blank=True, null=True)
    is_active = models.BooleanField('启用', default=True)
    order = models.PositiveIntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'

    def __str__(self):
        return self.name
