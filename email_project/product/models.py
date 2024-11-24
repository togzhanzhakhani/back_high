from django.db import models

class ProductDataset(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    file = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                              default='pending', db_index=True)
    def __str__(self):
        return f"Dataset {self.id} - {self.status}"
