from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = CustomUser.objects.get(username=attrs['username'])
        if user.two_factor_enabled and user.otp_code != attrs.get('otp_code', ''):
            raise AuthenticationFailed('Invalid OTP code.')
        return super().validate(attrs)