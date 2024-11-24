from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmailForm, TaskForm
from .tasks import send_email_task

def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']

            send_email_task.delay(recipient, subject, body)
            messages.success(request, 'Email is being sent in the background!')
            return redirect('send_email')
    else:
        form = EmailForm()
    return render(request, 'tasks/send_email.html', {'form': form})


def create_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task-success') 
    else:
        form = TaskForm()
    
    return render(request, 'tasks/create_task.html', {'form': form})


import logging

logger = logging.getLogger('django')

def monitor_activity(request):
    if request.method == "POST":
        suspicious_activity_detected = False 
        if suspicious_activity_detected:
            logger.warning(f"Suspicious activity detected for user: {request.user.username}")
