from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Order, OrderItem
from cart.cart import Cart
from customer.decorators import customer_required

# Create your views here.

@login_required
@customer_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        success = False
        return render(request,
                'orders/created.html',
                {'success': success})
    else:
        order = Order.objects.create(customer=request.user.customer)
        for item in cart.get_all_items():
            OrderItem.objects.create(order=order,
                                food=item.food,
                                quantity=item.quantity,
                                price=item.price)
        cart.clear()
        order_items = OrderItem.objects.filter(order=order)
        success = True
        return render(request,
                    'orders/created.html',
                    {'order': order, 'order_items': order_items, 'success': success})