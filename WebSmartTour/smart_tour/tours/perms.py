from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.name == 'ADMIN'



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
