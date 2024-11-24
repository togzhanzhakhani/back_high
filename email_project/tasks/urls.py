from django.urls import path
from .views import send_email_view, create_task_view

urlpatterns = [
    path('send-email/', send_email_view, name='send_email'),
    path('create/', create_task_view, name='create-task'),
]
