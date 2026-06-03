from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import SiteConfig, FriendLink
from .serializers import SiteConfigSerializer, FriendLinkSerializer


def health_check(request):
    return JsonResponse({'status': 'ok'})


def readiness_check(request):
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False

    status_code = 200 if db_ok else 503
    return JsonResponse({
        'status': 'ready' if db_ok else 'not_ready',
        'database': 'ok' if db_ok else 'error',
    }, status=status_code)


class SiteConfigView(generics.RetrieveAPIView):
    serializer_class = SiteConfigSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return SiteConfig.get_solo()


class FriendLinkListView(generics.ListAPIView):
    serializer_class = FriendLinkSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return FriendLink.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        cache_key = 'friend_links_list'
        data = cache.get(cache_key)
        if data is not None:
            from rest_framework.response import Response
            return Response(data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 3600)
        return response
