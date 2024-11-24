from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator, RegexValidator
from encrypted_model_fields.fields import EncryptedCharField


class Email(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class Task(models.Model):
    title = EncryptedCharField(max_length=200)
    priority = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    due_date = models.DateField()
    related_url = models.URLField(validators=[URLValidator()], blank=True)

    def __str__(self):
        return self.title
