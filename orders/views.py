import requests
import json
import os

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Order, OrderItem
from cart.cart import Cart
from customer.decorators import customer_required
from .forms import CreateOrderForm
from location.models import DeliveryLocation
from .tasks import order_created_successfully
from coupons.models import CouponUsed
from foods.models import Food
from foods.forms import BuyNowForm

# Create your views here.

@require_POST
@login_required
@customer_required
def order_create_cash_payment(request):
    success = False
    cart = Cart(request)
    if len(cart) == 0:
        return render(request,
                'orders/created.html',
                {'success': success})
    else:
        form = CreateOrderForm(request,data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            delivery_location = DeliveryLocation.objects.get(id=cd['delivery_location'])
            order = Order.objects.create(customer=request.user.customer, payment_by_cash=True, delivery_location=delivery_location)
            if cart.coupon:
                coupon = cart.coupon
                order.coupon = coupon
                order.save()
                CouponUsed.objects.create(coupon=coupon, customer=request.user.customer)
            for item in cart.get_all_items():
                OrderItem.objects.create(order=order,
                                    food=item.food,
                                    quantity=item.quantity,
                                    price=item.price)
            cart.clear()
            # launch asynchronous task
            order_created_successfully.delay(order.id)
            order_items = OrderItem.objects.filter(order=order)
            success = True
        return render(request,
                    'orders/created.html',
                    {'order': order, 'order_items': order_items, 'success': success})


@csrf_exempt
def verify_payment(request):
    data = request.POST
    token = data['token']
    amount = data['amount']

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
    "token": token,
    "amount": amount,
    }
    headers = {
    "Authorization": os.getenv('KHALTI_SECRET_KEY'),
    }

    response = requests.post(url, payload, headers = headers)
    response_data = json.loads(response.text)
    status_code = str(response.status_code)

    if status_code == '400':
        response = JsonResponse(f"response_data['detail']", status=500)
        return response

    import pprint 
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response_data)
    
    return JsonResponse({'token': token,})


@require_POST
@login_required
@customer_required
def order_create_khalti_payment(request, token):
    success = False
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
            order = Order.objects.create(customer=request.user.customer, verified=True, delivery_location=delivery_location, transaction=token)
            if cart.coupon:
                coupon = cart.coupon
                order.coupon = coupon
                order.save()
                CouponUsed.objects.create(coupon=coupon, customer=request.user.customer)
            for item in cart.get_all_items():
                OrderItem.objects.create(order=order,
                                    food=item.food,
                                    quantity=item.quantity,
                                    price=item.price)
            cart.clear()
            # launch asynchronous task
            order_created_successfully.delay(order.id)
            order_items = OrderItem.objects.filter(order=order)
            success = True
        return render(request,
                    'orders/created.html',
                    {'order': order, 'order_items': order_items, 'success': success})


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


@require_POST
@login_required
@customer_required
def order_create_buy_now(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    success = False
    form = BuyNowForm(request,data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        delivery_location = DeliveryLocation.objects.get(id=cd['delivery_location'])
        order = Order.objects.create(customer=request.user.customer, payment_by_cash=True, delivery_location=delivery_location)
        OrderItem.objects.create(order=order,
                                    food=food,
                                    quantity=cd['quantity'],
                                    price=food.price)
        # launch asynchronous task
        order_created_successfully.delay(order.id)
        order_items = OrderItem.objects.filter(order=order)
        success = True
    return render(request,
                    'orders/created.html',
                    {'order': order, 'order_items': order_items, 'success': success})


@require_POST
@login_required
@customer_required
def order_create_buy_now_khalti_payment(request, food_id, token):
    food = get_object_or_404(Food, id=food_id)
    success = False
    form = BuyNowForm(request,data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        delivery_location = DeliveryLocation.objects.get(id=cd['delivery_location'])
        order = Order.objects.create(customer=request.user.customer, verified=True, delivery_location=delivery_location, transaction=token)
        OrderItem.objects.create(order=order,
                                    food=food,
                                    quantity=cd['quantity'],
                                    price=food.price)
        # launch asynchronous task
        order_created_successfully.delay(order.id)
        order_items = OrderItem.objects.filter(order=order)
        success = True
    return render(request,
                    'orders/created.html',
                    {'order': order, 'order_items': order_items, 'success': success})