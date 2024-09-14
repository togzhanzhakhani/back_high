from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', views.index),
    path('', include('blog.urls')),
]
