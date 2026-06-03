from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserProfileView, UserListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
