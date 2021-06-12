from django.db import models
from customer.models import Customer
from foods.models import Food
from location.models import DeliveryLocation

# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='order', on_delete=models.CASCADE)
    delivery_location = models.ForeignKey(DeliveryLocation, related_name='delivery_location', on_delete=models.CASCADE)
    transaction = models.CharField(max_length=250, default='')
    payment_by_cash = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Order {self.id} by customer {self.customer.user.username}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    food = models.ForeignKey(Food, related_name='order_items', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity