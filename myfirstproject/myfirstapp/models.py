from django.db import models
# Create your models here.
# models.py


class Travel(models.Model):
    city = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    destination = models.CharField(max_length=255)
    duration_days = models.PositiveIntegerField()
    image = models.ImageField(upload_to='travel_images/', null=True, blank=True)
    def __str__(self):
        return self.city
