from rest_framework.throttling import UserRateThrottle


class ProviderRateThrottle(UserRateThrottle):
    scope = 'provider'

    def allow_request(self, request, view):
        user = request.user
        if user.is_authenticated and user.role and user.role.name == 'PROVIDER':
            return super().allow_request(request, view)
        return True
