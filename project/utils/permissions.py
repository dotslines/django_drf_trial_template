from rest_framework.permissions import BasePermission


class AccountOwnerPermission(BasePermission):
    """
    checks if user tries to change an own profile
    """
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id