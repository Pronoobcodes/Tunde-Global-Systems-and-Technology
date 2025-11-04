from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Customer(AbstractUser):
    username = models.CharField(max_length=200, null=True, unique=True)
    full_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=15, null=True, unique=True)
    email = models.EmailField(unique=True, null=True)
    address = models.CharField(max_length=255, null=True)
    user_cart = models.CharField(max_length=200, blank=True, null=True)

    