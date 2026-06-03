from django.contrib.auth.models import User
from django.db import models


class Comment(models.Model):
    """评论模型（支持楼中楼）"""
    article = models.ForeignKey(
        'articles.Article',
        verbose_name='文章',
        related_name='comments',
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='父评论',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        verbose_name='作者',
        related_name='comments',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    nickname = models.CharField('昵称', max_length=50, default='匿名用户')
    content = models.TextField('内容')
    is_approved = models.BooleanField('已审核', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论'
        indexes = [
            models.Index(fields=['article', '-created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.nickname} on {self.article.title}'

    def get_replies_count(self):
        """获取回复数量"""
        return self.replies.count()
