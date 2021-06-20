from django.db import models

from customer.models import Customer
from foods.models import Food


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    coupon_code = models.CharField(max_length=50, )

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'Cart for customer {self.customer.user.username}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,
                    related_name='items',
                    on_delete=models.CASCADE)
    food = models.ForeignKey(Food,
                        related_name='cart_items',
                        on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)
    
    def get_total_price(self):
        return self.price * self.quantity