from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    discounted_price = models.FloatField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['shop']),
            models.Index(fields=['category']),
            models.Index(fields=['discount']),
        ]

    def save(self, *args, **kwargs):
        if self.discount:
            self.discounted_price = self.price * (1 - self.discount / 100)
        else:
            self.discounted_price = self.price 

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
