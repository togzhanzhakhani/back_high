from django import forms
from .models import Task
from django.utils.timezone import now

class EmailForm(forms.Form):
    recipient = forms.EmailField(label='Recipient Email')
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'priority', 'due_date', 'related_url']

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date < now().date():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date
