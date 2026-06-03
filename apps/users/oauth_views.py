import os
import secrets
import urllib.parse
import urllib.request
import json
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import SocialAccount, UserProfile

logger = logging.getLogger(__name__)


def _http_post_json(url, data, headers=None):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, headers=headers or {})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def _http_get_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def _issue_jwt_redirect(user):
    refresh = RefreshToken.for_user(user)
    frontend = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
    params = urllib.parse.urlencode({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })
    return HttpResponseRedirect(f'{frontend}/oauth/callback?{params}')


def _get_or_create_oauth_user(provider, uid, username, email='', extra=None):
    account = SocialAccount.objects.filter(provider=provider, uid=str(uid)).select_related('user').first()
    if account:
        return account.user

    base_username = username or f'{provider}_{uid}'
    unique_username = base_username
    counter = 1
    while User.objects.filter(username=unique_username).exists():
        unique_username = f'{base_username}_{counter}'
        counter += 1

    user = User.objects.create_user(
        username=unique_username,
        email=email or '',
        password=secrets.token_urlsafe(32),
    )
    UserProfile.objects.get_or_create(user=user)
    SocialAccount.objects.create(
        user=user, provider=provider, uid=str(uid),
        extra_data=extra or {}
    )
    return user


class GitHubOAuthStartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client_id = os.environ.get('GITHUB_CLIENT_ID', '')
        if not client_id:
            return Response({'error': 'GitHub OAuth 未配置'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        redirect_uri = request.build_absolute_uri('/api/auth/oauth/github/callback/')
        params = urllib.parse.urlencode({
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'scope': 'read:user user:email',
        })
        return Response({'authorization_url': f'https://github.com/login/oauth/authorize?{params}'})


class GitHubOAuthCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({'error': '缺少授权码'}, status=status.HTTP_400_BAD_REQUEST)

        client_id = os.environ.get('GITHUB_CLIENT_ID', '')
        client_secret = os.environ.get('GITHUB_CLIENT_SECRET', '')
        if not client_id or not client_secret:
            return Response({'error': 'GitHub OAuth 未配置'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            token_data = _http_post_json(
                'https://github.com/login/oauth/access_token',
                {
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'code': code,
                },
                headers={'Accept': 'application/json'},
            )
            access_token = token_data.get('access_token')
            if not access_token:
                return Response({'error': '获取 access_token 失败'}, status=status.HTTP_400_BAD_REQUEST)

            user_data = _http_get_json(
                'https://api.github.com/user',
                headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'},
            )
            email = user_data.get('email') or ''
            if not email:
                emails = _http_get_json(
                    'https://api.github.com/user/emails',
                    headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'},
                )
                for item in emails:
                    if item.get('primary'):
                        email = item.get('email', '')
                        break

            user = _get_or_create_oauth_user(
                'github', user_data['id'], user_data.get('login'),
                email, user_data
            )
            return _issue_jwt_redirect(user)
        except Exception as e:
            logger.exception('GitHub OAuth failed')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WechatOAuthStartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        appid = os.environ.get('WECHAT_APP_ID', '')
        if not appid:
            return Response({'error': '微信 OAuth 未配置'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        redirect_uri = request.build_absolute_uri('/api/auth/oauth/wechat/callback/')
        params = urllib.parse.urlencode({
            'appid': appid,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'snsapi_login',
            'state': 'wechat_login',
        })
        return Response({'authorization_url': f'https://open.weixin.qq.com/connect/qrconnect?{params}#wechat_redirect'})


class WechatOAuthCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({'error': '缺少授权码'}, status=status.HTTP_400_BAD_REQUEST)

        appid = os.environ.get('WECHAT_APP_ID', '')
        secret = os.environ.get('WECHAT_APP_SECRET', '')
        if not appid or not secret:
            return Response({'error': '微信 OAuth 未配置'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            token_data = _http_get_json(
                f'https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code'
            )
            access_token = token_data.get('access_token')
            openid = token_data.get('openid')
            if not access_token or not openid:
                err_msg = token_data.get('errmsg', '获取微信 token 失败')
                return Response({'error': err_msg}, status=status.HTTP_400_BAD_REQUEST)

            user_data = _http_get_json(
                f'https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}'
            )
            nickname = user_data.get('nickname', f'wechat_{openid}')
            user = _get_or_create_oauth_user(
                'wechat', openid, nickname,
                '', user_data
            )
            return _issue_jwt_redirect(user)
        except Exception as e:
            logger.exception('Wechat OAuth failed')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
