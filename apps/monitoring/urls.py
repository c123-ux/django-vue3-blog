from django.urls import path
from .views import (
    MonitorServerListView,
    MonitorMetricHistoryView,
    MetricReportView,
    LocalMetricsView,
)

urlpatterns = [
    path('servers/', MonitorServerListView.as_view(), name='monitor-servers'),
    path('servers/<int:server_id>/metrics/', MonitorMetricHistoryView.as_view(), name='monitor-history'),
    path('report/', MetricReportView.as_view(), name='monitor-report'),
    path('local/', LocalMetricsView.as_view(), name='monitor-local'),
]
