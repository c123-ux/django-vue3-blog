from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    """便签笔记"""
    author = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    tags = models.CharField('标签', max_length=200, blank=True, help_text='逗号分隔')
    is_public = models.BooleanField('公开', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = '便签'
        verbose_name_plural = '便签'

    def __str__(self):
        return self.title

    def get_tags_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]
