from django.urls import path
from .views import upload_product_dataset, task_progress, get_datasets_by_status_view

urlpatterns = [
    path('upload/', upload_product_dataset, name='upload_product_dataset'),
    path('task-progress/<task_id>/', task_progress, name='task_progress'),
    path('datasets/<str:status>/', get_datasets_by_status_view, name='get_datasets_by_status'),
]
