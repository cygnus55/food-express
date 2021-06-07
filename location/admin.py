from django.contrib import admin
from .models import RestaurantLocation, DeliveryLocation

# Register your models here.

admin.site.register(RestaurantLocation)

admin.site.register(DeliveryLocation)
