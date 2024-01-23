from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date, datetime

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Use a more secure method for storing passwords
    
    birth_date = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username


class Promotion(models.Model):
    name = models.CharField(max_length=255)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.name


class Travel(models.Model):
    city = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    destination = models.CharField(max_length=255)
    duration_days = models.PositiveIntegerField()
    image = models.ImageField(upload_to='travel_images/', null=True, blank=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.city


class Reservation(models.Model):
    my_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)
    mydate = models.DateField(default=datetime.now)
    name = models.CharField(max_length=200,default='')
    email = models.EmailField(default='')
    address = models.CharField(max_length=200,default='')
    cardnumber = models.CharField(max_length=16,default='')
    expiration = models.DateField(default=date(1970, 1, 1))
    cvv = models.CharField(max_length=3,default='')