from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

from restaurants.models import Restaurant
from customer.models import Customer

# Create your models here.

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(active=True)

class Coupon(models.Model):
    code = models.CharField(max_length=50,unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, related_name='coupon', on_delete=models.CASCADE)

    objects = models.Manager()
    activated = ActiveManager()

    def ___str___(self):
        return f"{self.code} for {self.restaurant.name}"


class CouponUsed(models.Model):
    coupon = models.ForeignKey(Coupon, related_name='coupon', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="used", on_delete=models.CASCADE)
    used_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("coupon", "customer"),)
    
    def __str__(self):
        return f'{self.customer.user.username} uses {self.coupon.code}'