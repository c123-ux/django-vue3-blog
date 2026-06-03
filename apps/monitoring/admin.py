from django.contrib import admin
from .models import MonitorServer, MonitorMetric


@admin.register(MonitorServer)
class MonitorServerAdmin(admin.ModelAdmin):
    list_display = ['name', 'hostname', 'is_active', 'created_at']
    readonly_fields = ['token']


@admin.register(MonitorMetric)
class MonitorMetricAdmin(admin.ModelAdmin):
    list_display = ['server', 'cpu_percent', 'memory_percent', 'disk_percent', 'reported_at']
    list_filter = ['reported_at']
