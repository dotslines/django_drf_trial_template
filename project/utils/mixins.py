from rest_framework.permissions import (
    IsAdminUser, IsAuthenticated, AllowAny, BasePermission
)
from .permissions import AccountOwnerPermission


class DynamicPaginationMixin(object):
    """
    Dynamically changes pagination status concerning to request query
    """
    def paginate_queryset(self, queryset):
        pagination = self.request.query_params.get("pagination", "true")
        if bool(pagination):
            return None

        return super().paginate_queryset(queryset)


class AccountsPermissionMixin(object):
    """
    returns permission classes based on action
    """
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny()]
        elif self.action in ('update', 'partial_update', 'delete'):
            permission_classes = [AccountOwnerPermission(), IsAuthenticated()]
        else:
            permission_classes = [IsAuthenticated()]
        return permission_classes
