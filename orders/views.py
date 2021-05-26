from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.contrib.admin.views.decorators import staff_member_required

from .models import Order, OrderItem
from cart.cart import Cart
from customer.decorators import customer_required

# Create your views here.

@login_required
@customer_required
def order_create(request, payment:str='pay-by-cash'):
    cart = Cart(request)
    if len(cart) == 0:
        success = False
        return render(request,
                'orders/created.html',
                {'success': success})
    else:
        if payment == 'pay-by-cash':
            payment_by_cash = True
        elif payment == 'pay-by-khalti':
            payment_by_cash = False
        order = Order.objects.create(customer=request.user.customer, payment_by_cash=payment_by_cash)
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



def order_list(request):
    queryset = list(Order.objects.filter(payment_by_cash=True, verified=False))
    data = serializers.serialize("json", queryset)
    # json.dump(queryset, open('order.json', 'w'))
    return JsonResponse({'orders': data})


@login_required
@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})