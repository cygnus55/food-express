from django.db import models

from accounts.models import User
from orders.models import Order
from phonenumber_field.modelfields import PhoneNumberField


class DeliveryPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='delivery_person')
    full_name = models.CharField(db_index=True, max_length=200)
    profile_pic = models.ImageField(upload_to='delivery_person/profile_pic', blank=True)
    phone_no = PhoneNumberField(region='NP')
    created = models.TimeField(auto_now_add=True)
    updated = models.TimeField(auto_now=True)

    class Meta:
        ordering = ('full_name',)
        index_together = (('id', 'user'),)
    
    def __str__(self):
        return f'Delivery Person: {self.full_name} for user {self.user.username}'


class OrdersDesignation(models.Model):
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE, related_name='orders')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='designation')
    
    def __str__(self):
        return f'OrdersDesignation: Order {self.order.id} <- DeliveryPerson {self.delivery_person}'