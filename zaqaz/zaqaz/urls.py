from django.contrib import admin
from django.urls import path, include
from debug_toolbar import urls as debug_toolbar_urls
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('custom_auth.urls')),
    path('api/', include('products.urls')),
    path('api/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar_urls)),  
    ]
