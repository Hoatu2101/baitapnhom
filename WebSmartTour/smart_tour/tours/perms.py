from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission

class CommentOwner(IsAuthenticated):
    def has_object_permission(self, request, view, comment):
        return super().has_permission(request, view) and request.user == comment.user


class IsProvider(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role and
            request.user.role.name == 'PROVIDER' and
            request.user.is_verified
        )

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role and
            request.user.role.name == 'CUSTOMER'
        )
