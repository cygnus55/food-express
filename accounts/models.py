from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_customer = models.BooleanField(default=False)
    is_restaurant = models.BooleanField(default=False)
    is_delivery_person = models.BooleanField(default=False)