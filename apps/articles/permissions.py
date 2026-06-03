from rest_framework import permissions


class IsAuthorOrStaff(permissions.BasePermission):
    """仅文章作者或管理员可修改/删除"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_staff
