from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class IsProvider(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and
            user.role and
            user.role.name == 'PROVIDER' and
            user.is_verified
        )


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and
            user.role and
            user.role.name == 'CUSTOMER'
        )

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            request.user.is_authenticated and
            hasattr(obj, 'user') and
            obj.user == request.user
        )


class ReadOnly(BasePermission):
    """
    Chỉ cho phép GET, HEAD, OPTIONS
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
