from rest_framework import serializers
from .models import MonitorServer, MonitorMetric


class MonitorMetricSerializer(serializers.ModelSerializer):
    server_name = serializers.CharField(source='server.name', read_only=True)

    class Meta:
        model = MonitorMetric
        fields = [
            'id', 'server_name', 'cpu_percent', 'memory_percent', 'disk_percent',
            'load_avg', 'network_in', 'network_out', 'uptime', 'reported_at'
        ]


class MonitorServerSerializer(serializers.ModelSerializer):
    latest_metric = serializers.SerializerMethodField()

    class Meta:
        model = MonitorServer
        fields = ['id', 'name', 'hostname', 'description', 'is_active', 'latest_metric', 'created_at']

    def get_latest_metric(self, obj):
        metric = obj.metrics.first()
        if not metric:
            return None
        return MonitorMetricSerializer(metric).data


class MetricReportSerializer(serializers.Serializer):
    token = serializers.CharField()
    hostname = serializers.CharField(required=False, allow_blank=True)
    cpu_percent = serializers.FloatField(min_value=0, max_value=100)
    memory_percent = serializers.FloatField(min_value=0, max_value=100)
    disk_percent = serializers.FloatField(min_value=0, max_value=100)
    load_avg = serializers.FloatField(required=False, default=0)
    network_in = serializers.IntegerField(required=False, default=0)
    network_out = serializers.IntegerField(required=False, default=0)
    uptime = serializers.IntegerField(required=False, default=0)
