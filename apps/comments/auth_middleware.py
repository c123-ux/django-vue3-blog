from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model


class JWTAuthMiddleware:
    """WebSocket JWT 认证中间件"""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'websocket':
            return await self.inner(scope, receive, send)

        scope['user'] = AnonymousUser()
        query_string = scope.get('query_string', b'').decode()
        token = None
        for param in query_string.split('&'):
            if param.startswith('token='):
                token = param.split('=', 1)[1]

        if token:
            try:
                validated = AccessToken(token)
                user_id = validated['user_id']
                User = get_user_model()
                scope['user'] = await database_sync_to_async(User.objects.get)(id=user_id)
            except Exception:
                scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)
