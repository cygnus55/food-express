from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

from restaurants.models import Restaurant
# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50,unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, related_name='coupon', on_delete=models.CASCADE)

    def ___str___(self):
        return f"{self.code} for {self.restaurant.name}" 