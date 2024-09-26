from django.contrib import admin
from django.urls import path, include
from blog import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', views.index),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
