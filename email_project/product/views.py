from django.shortcuts import render
from django.contrib import messages
from .forms import ProductDatasetUploadForm
from tasks.tasks import process_csv
from django.http import JsonResponse
from celery.result import AsyncResult
from .models import ProductDataset


def upload_product_dataset(request):
    if request.method == 'POST':
        form = ProductDatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save()
            dataset.status = 'pending'  
            dataset.save()
            task = process_csv.delay(dataset.id)
            messages.success(request, 'File uploaded successfully!')
            return render(request, 'products/upload_dataset.html', {'form': form, 'task_id': task.id})
        else:
            messages.error(request, 'Failed to upload file. Please try again.')
    else:
        form = ProductDatasetUploadForm()

    return render(request, 'products/upload_dataset.html', {'form': form})

def task_progress(request, task_id):
    task = AsyncResult(task_id)
    if task.state == 'PROGRESS':
        response_data = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
        }
    elif task.state == 'SUCCESS':
        response_data = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
        }
    else:
        response_data = {'state': task.state}
    return JsonResponse(response_data)

from django.core.cache import cache

def get_datasets_by_status_view(request, status):
    cache_key = f'datasets_status_{status}'
    datasets = cache.get(cache_key)

    if not datasets:
        datasets = list(ProductDataset.objects.filter(status=status).values())
        cache.set(cache_key, datasets, timeout=60 * 15)

    return JsonResponse({"datasets": datasets})