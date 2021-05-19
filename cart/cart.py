from decimal import Decimal
from django.conf import settings

from .models import Cart as cart_model, CartItem

class Cart(object):

    def __init__(self,request):
        self.customer = request.user.customer
        try:
            cart = self.customer.cart
        except Exception:
            cart = cart_model.objects.create(customer=self.customer)
        self.cart = cart
    
    def add(self, food, quantity=1, override_quantity=False):
        try:
            cart_item = CartItem.objects.get(cart=self.cart, food=food)
        except:
            cart_item = CartItem.objects.create(cart=self.cart, food=food,
                                    quantity=0, price=food.price)
        
        if override_quantity:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()
    
    def remove(self, food):
        cart_item = CartItem.objects.get(cart=self.cart, food=food)
        if cart_item:
            cart_item.delete()
    
    def __len__(self):
        cart_items = self.get_all_items()
        return sum(item.quantity for item in cart_items)

    def get_total_price(self):
        cart_items = self.get_all_items()
        return sum(Decimal(item.price) * item.quantity for item in cart_items)
    
    def get_all_items(self):
        return CartItem.objects.filter(cart=self.cart)

    def clear(self):
        self.cart.delete()