from django.urls import path
from .views import SiteConfigView, FriendLinkListView

urlpatterns = [
    path('', SiteConfigView.as_view(), name='site-config'),
    path('friend-links/', FriendLinkListView.as_view(), name='friend-links'),
]
