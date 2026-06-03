from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class LoginRateThrottle(UserRateThrottle):
    """
    登录接口限流
    每分钟最多5次尝试
    """
    scope = 'login'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return f'{self.scope}_{ident}'
    
    def throttle_failure(self):
        logger.warning(f'登录限流触发：IP {self.get_ident(self.request)}')
        return Response(
            {'detail': '登录尝试过于频繁，请稍后再试'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )


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


class UploadRateThrottle(UserRateThrottle):
    """
    上传接口限流
    每分钟最多10次上传
    """
    scope = 'upload'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return f'{self.scope}_{ident}'


class BurstRateThrottle(UserRateThrottle):
    """
    突发流量限流
    防止短时间内大量请求
    """
    scope = 'burst'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return f'{self.scope}_{ident}'


class AnonBurstRateThrottle(UserRateThrottle):
    """
    匿名用户突发流量限流
    更严格的限制
    """
    scope = 'anon_burst'
    
    def get_cache_key(self, request, view):
        return f'{self.scope}_{self.get_ident(request)}'