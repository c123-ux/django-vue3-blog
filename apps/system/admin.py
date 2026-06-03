from django.contrib import admin
from .models import SiteConfig, FriendLink


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'author_name', 'icp_number']


@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_active', 'order']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']
