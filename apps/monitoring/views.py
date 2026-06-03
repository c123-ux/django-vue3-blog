from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MonitorServer, MonitorMetric
from .serializers import MonitorServerSerializer, MonitorMetricSerializer, MetricReportSerializer


class MonitorServerListView(generics.ListAPIView):
    """监控服务器列表（含最新指标）"""
    serializer_class = MonitorServerSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return MonitorServer.objects.filter(is_active=True).prefetch_related('metrics')


class MonitorMetricHistoryView(generics.ListAPIView):
    """某服务器历史指标"""
    serializer_class = MonitorMetricSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        server_id = self.kwargs['server_id']
        return MonitorMetric.objects.filter(
            server_id=server_id, server__is_active=True
        ).select_related('server')[:100]


class MetricReportView(APIView):
    """监控客户端上报指标"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MetricReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            server = MonitorServer.objects.get(token=data['token'], is_active=True)
        except MonitorServer.DoesNotExist:
            return Response({'error': '无效的监控令牌'}, status=status.HTTP_403_FORBIDDEN)

        if data.get('hostname'):
            server.hostname = data['hostname']
            server.save(update_fields=['hostname'])

        metric = MonitorMetric.objects.create(
            server=server,
            cpu_percent=data['cpu_percent'],
            memory_percent=data['memory_percent'],
            disk_percent=data['disk_percent'],
            load_avg=data.get('load_avg', 0),
            network_in=data.get('network_in', 0),
            network_out=data.get('network_out', 0),
            uptime=data.get('uptime', 0),
        )

        # 只保留最近 1000 条记录
        old_ids = list(server.metrics.values_list('id', flat=True)[1000:])
        if old_ids:
            MonitorMetric.objects.filter(id__in=old_ids).delete()

        return Response({'status': 'ok', 'metric_id': metric.id})


class LocalMetricsView(APIView):
    """本机实时指标（Django 服务器）"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            import os
            import psutil
            import time
            disk_path = 'C:\\' if os.name == 'nt' else '/'
            return Response({
                'cpu_percent': psutil.cpu_percent(interval=0.5),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage(disk_path).percent,
                'load_avg': (psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0),
                'uptime': int(time.time() - psutil.boot_time()),
            })
        except ImportError:
            return Response({'error': 'psutil 未安装'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
