from rest_framework.throttling import UserRateThrottle

class RoleBasedThrottle(UserRateThrottle):
    rate = '5/hour' 
    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.user.role == 'admin':
            self.rate = '100/hour' 
        return super().get_cache_key(request, view)
