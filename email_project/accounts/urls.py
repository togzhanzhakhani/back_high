from django.urls import path
from .views import register_view, enable_2fa_view, dashboard_view, custom_login_view, verify_otp_view, CustomTokenObtainPairView
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', custom_login_view, name='login'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('enable-2fa/', enable_2fa_view, name='enable_2fa'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
