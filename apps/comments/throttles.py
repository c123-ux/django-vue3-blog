from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class CommentRateThrottle(UserRateThrottle):
    """
    评论接口限流
    每分钟最多20次评论
    """
    scope = 'comment'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return f'{self.scope}_{ident}'