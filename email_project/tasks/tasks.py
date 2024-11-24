from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import time
from product.models import ProductDataset

@shared_task(bind=True, max_retries=3)
def send_email_task(self, recipient, subject, body):
    try:
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [recipient],
            fail_silently=False,
        )
        return 'Email sent successfully!'
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)


@shared_task
def process_csv(dataset_id):
    try:
        dataset = ProductDataset.objects.get(id=dataset_id)
        file_path = dataset.file.path
        total_lines = sum(1 for _ in open(file_path)) 
        processed_lines = 0
        with open(file_path, 'r') as file:
            for line in file:
                processed_lines += 1
                time.sleep(0.1) 
                process_csv.update_state(state='PROGRESS', meta={'current': processed_lines, 'total': total_lines})
        dataset.status = 'Processed'
        dataset.save()
        return {'status': 'Task completed!'}
    except Exception as e:
        dataset.status = 'Error'
        dataset.save()
        return f"Error processing dataset {dataset_id}: {str(e)}"
