from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from .models import Order, OrderItem
from cart.cart import Cart
from customer.decorators import customer_required
from .forms import CreateOrderForm
from location.models import DeliveryLocation

# Create your views here.

@require_POST
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
        form = CreateOrderForm(request,data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            delivery_location = DeliveryLocation.objects.get(id=cd['delivery_location'])
            if cd['payment_method'] == 'pay-by-cash':
                payment_by_cash = True
            elif cd['payment_method'] == 'pay-by-khalti':
                payment_by_cash = False
        order = Order.objects.create(customer=request.user.customer, payment_by_cash=payment_by_cash, delivery_location=delivery_location)
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


@login_required
@staff_member_required
def verify_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.verified = True
    order.save()
    return redirect('orders:order_detail', order_id=order_id)