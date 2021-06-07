from django.db import models

from restaurants.models import Restaurant
from customer.models import Customer

# Create your models here.


class RestaurantLocation(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    address = models.CharField(max_length=250)
    restaurant = models.OneToOneField(
        Restaurant,
        related_name='location',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'location for restaurant {self.restaurant.name}'


class DeliveryLocation(models.Model):
    title = models.CharField(max_length=250)
    longitude = models.FloatField()
    latitude = models.FloatField()
    address = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, related_name='location', on_delete=models.CASCADE)

    def __str__(self):
        return self.title