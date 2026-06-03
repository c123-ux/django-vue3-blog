from django.contrib import admin
from .models import UserProfile, SocialAccount


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location']
    search_fields = ['user__username']


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'provider', 'uid', 'created_at']
    list_filter = ['provider']
