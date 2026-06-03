from rest_framework import serializers
from .models import SiteConfig, FriendLink


class SiteConfigSerializer(serializers.ModelSerializer):
    running_days = serializers.SerializerMethodField()

    class Meta:
        model = SiteConfig
        fields = [
            'site_name', 'site_description', 'site_keywords',
            'author_name', 'author_bio', 'author_avatar',
            'icp_number', 'github_url', 'notice', 'start_date', 'running_days'
        ]

    def get_running_days(self, obj):
        if not obj.start_date:
            return 0
        from django.utils import timezone
        return (timezone.now().date() - obj.start_date).days


class FriendLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendLink
        fields = ['id', 'name', 'url', 'description', 'logo', 'order']
