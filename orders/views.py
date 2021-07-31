from django.http.response import HttpResponse
import requests
import json
import os
import weasyprint

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template.loader import render_to_string

from .models import Order, OrderItem
from cart.cart import Cart
from customer.decorators import customer_required
from .forms import CreateOrderForm
from location.models import DeliveryLocation
from delivery_person.models import OrdersDesignation
from .tasks import order_created_successfully, send_invoice
from coupons.models import Coupon, CouponUsed
from foods.models import Food
from foods.forms import BuyNowForm
from orders.forms import CreateOrderForm, OrderDesignateForm
from coupons.forms import CouponApplyForm

# Create your views here.


def ordered_food_and_restaurant_available(order_items):
    for food in order_items:
        if food.restaurant.available and food.available:
            pass
        else:
            return False
    return True


def ordered_restaurant_open(order_items):
    for food in order_items:
        if food.restaurant.get_open_status:
            pass
        else:
            return False
    return True

@require_POST
@login_required
@customer_required
def order_create_cash_payment(request):
    cart = Cart(request)
    if len(cart) == 0:
        return render(request,
                'orders/created.html',
                {'response': 'cart_empty'})
    else:
        form = CreateOrderForm(request,data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            delivery_location = DeliveryLocation.objects.get(id=cd['delivery_location'])

            if not ordered_food_and_restaurant_available(cart.get_foods_list()):
                return render(request,
                    'orders/created.html',
                    {'response': 'not_available'})
            
            if not ordered_restaurant_open(cart.get_foods_list()):
                return render(request,
                    'orders/created.html',
                    {'response': 'restaurant_close'})

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
            message = f"Invoice for your order is attached in the pdf file. Your order is not verified. You would soon get call from our administration."
            send_invoice.delay(order.id, message)
            order_items = OrderItem.objects.filter(order=order)
        return render(request,
                    'orders/created.html',
                    {'order': order, 'order_items': order_items, 'response': 'success'})


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
    cart = Cart(request)
    if len(cart) == 0:
        return render(request,
                'orders/created.html',
                {'response': 'cart_empty'})
    else:
        form = CreateOrderForm(request,data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            delivery_location = DeliveryLocation.objects.get(id=cd['delivery_location'])

            if not ordered_food_and_restaurant_available(cart.get_foods_list()):
                return render(request,
                    'orders/created.html',
                    {'response': 'not_available'})
            
            if not ordered_restaurant_open(cart.get_foods_list()):
                return render(request,
                    'orders/created.html',
                    {'response': 'restaurant_close'})

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
            message = f"Invoice for your order is attached in the pdf file. Your order is verified. You would soon get our delivery person at your door."
            send_invoice.delay(order.id, message)
            order_items = OrderItem.objects.filter(order=order)
        return render(request,
                    'orders/created.html',
                    {'order': order, 'order_items': order_items, 'response': 'success'})


@login_required
@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    try:
        delivery_person = OrdersDesignation.objects.get(order=order_id).delivery_person
    except Exception:
        delivery_person = None
    form = OrderDesignateForm()
    return render(request, 
            'orders/order_detail.html', 
            {
                'order': order, 
                'delivery_person': delivery_person,
                'form': form,
            })


@login_required
@staff_member_required
def verify_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.verified = True
    order.save()
    return redirect('orders:order_detail', order_id=order_id)


@login_required
@staff_member_required
def unverify_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    try:
        od = OrdersDesignation.objects.get(order=order_id)
        od.delete()
    except Exception:
        pass
    order.verified = False
    order.save()
    return redirect('orders:order_detail', order_id=order_id)


@require_POST
@login_required
@customer_required
def order_create_buy_now(request, food_id, quantity, coupon=''):
    if coupon:
        coupon_code = Coupon.objects.get(code__iexact = coupon)
        try:
            CouponUsed.objects.get(coupon=coupon_code, customer=request.user.customer)
            return render(request,
                'orders/created.html',
                {'response': 'coupon_already_used'},)
        except Exception:
            pass
    food = get_object_or_404(Food, id=food_id)
    form = BuyNowForm(request,data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        delivery_location = DeliveryLocation.objects.get(id=cd['delivery_location'])

        items = [food,]
        if not ordered_food_and_restaurant_available(items):
            return render(request,
                'orders/created.html',
                {'response': 'not_available'})
            
        if not ordered_restaurant_open(items):
            return render(request,
                'orders/created.html',
                {'response': 'restaurant_close'})

        order = Order.objects.create(customer=request.user.customer, payment_by_cash=True, delivery_location=delivery_location)
        if coupon:
            order.coupon = Coupon.objects.get(code__iexact = coupon)
            order.save()
            CouponUsed.objects.create(coupon=order.coupon, customer=request.user.customer)
        OrderItem.objects.create(order=order,
                                    food=food,
                                    quantity=quantity,
                                    price=food.get_selling_price)
        # launch asynchronous task
        order_created_successfully.delay(order.id)
        message = f"Invoice for your order is attached in the pdf file. Your order is not verified. You would soon get call from our administration."
        send_invoice.delay(order.id, message)
        order_items = OrderItem.objects.filter(order=order)
        return render(request,
                    'orders/created.html',
                    {'order': order, 'order_items': order_items, 'response': 'success'})
    return render(request,
                'orders/created.html',
                {'response': 'error'},)


@require_POST
@login_required
@customer_required
def order_create_buy_now_khalti_payment(request, food_id, quantity, token, coupon=''):
    if coupon:
        coupon_code = Coupon.objects.get(code__iexact = coupon)
        try:
            CouponUsed.objects.get(coupon=coupon_code, customer=request.user.customer)
            return render(request,
                'orders/created.html',
                {'response': 'coupon_already_used'},)
        except Exception:
            pass
    food = get_object_or_404(Food, id=food_id)
    form = BuyNowForm(request,data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        delivery_location = DeliveryLocation.objects.get(id=cd['delivery_location'])
        
        items = [food,]
        if not ordered_food_and_restaurant_available(items):
            return render(request,
                'orders/created.html',
                {'response': 'not_available'})
            
        if not ordered_restaurant_open(items):
            return render(request,
                'orders/created.html',
                {'response': 'restaurant_close'})
        
        order = Order.objects.create(customer=request.user.customer, verified=True, delivery_location=delivery_location, transaction=token)
        if coupon:
            order.coupon = Coupon.objects.get(code__iexact = coupon)
            order.save()
            CouponUsed.objects.create(coupon=order.coupon, customer=request.user.customer)
        OrderItem.objects.create(order=order,
                                    food=food,
                                    quantity=quantity,
                                    price=food.get_selling_price)
        # launch asynchronous task
        order_created_successfully.delay(order.id)
        message = f"Invoice for your order is attached in the pdf file. Your order is verified. You would soon get our delivery person at your door."
        send_invoice.delay(order.id, message)
        order_items = OrderItem.objects.filter(order=order)
        return render(request,
                        'orders/created.html',
                        {'order': order, 'order_items': order_items, 'response': 'success'})
    return render(request,
                'orders/created.html',
                {'response': 'error'},)


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    paid = ((not order.verified) and (not order.payment_by_cash)) or (order.verified and (not order.payment_by_cash)) or order.complete
    html = render_to_string('orders/pdf.html', {'order': order, 'payment_received': paid})

    response = HttpResponse(content_type='application/pdf')
    response['content-Disposition'] = f'filename=foodexpress_order_{order.id}.pdf'

    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'orders/css/pdf.css')])
    return response


@customer_required
def reorder(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    create_order_form = CreateOrderForm(request)
    coupon_apply_form = CouponApplyForm()

    foods = [item.food for item in order.items.all()]
    available = any([food.restaurant.available and food.available for food in foods])
    open_status = any([food.restaurant.get_open_status for food in foods])

    return render(
            request,
            'orders/reorder.html', 
            {
                'order': order,
                'create_order_form': create_order_form,
                'coupon_apply_form': coupon_apply_form,
                'available' : available,
                'open_status': open_status,
            })


@require_POST
@login_required
@customer_required
def create_order_reorder(request, order_id, coupon=''):
    if coupon:
        coupon_code = Coupon.objects.get(code__iexact = coupon)
        try:
            CouponUsed.objects.get(coupon=coupon_code, customer=request.user.customer)
            return render(request,
                'orders/created.html',
                {'response': 'coupon_already_used'},)
        except Exception:
            pass
    old_order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    form = CreateOrderForm(request,data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        delivery_location = DeliveryLocation.objects.get(id=cd['delivery_location'])

        foods = [item.food for item in old_order.items.all()]
        available = any([food.restaurant.available and food.available for food in foods])
        if not available:
            return render(request,
                'orders/created.html',
                {'response': 'not_available'})
        
        open_status = any([food.restaurant.get_open_status for food in foods])
        if not open_status:
            return render(request,
                'orders/created.html',
                {'response': 'restaurant_close'})

        order = Order.objects.create(customer=request.user.customer, payment_by_cash=True, delivery_location=delivery_location)
        if coupon:
            order.coupon = Coupon.objects.get(code__iexact = coupon)
            order.save()
            CouponUsed.objects.create(coupon=order.coupon, customer=request.user.customer)
        for item in old_order.items.all():
            if item.food.available:
                OrderItem.objects.create(order=order,
                                    food=item.food,
                                    quantity=item.quantity,
                                    price=item.food.get_selling_price)
        # launch asynchronous task
        order_created_successfully.delay(order.id)
        message = f"Invoice for your order is attached in the pdf file. Your order is not verified. You would soon get call from our administration."
        send_invoice.delay(order.id, message)
        order_items = OrderItem.objects.filter(order=order)
        return render(request,
                    'orders/created.html',
                    {'order': order, 'order_items': order_items, 'response': 'success'})
    return render(request,
                'orders/created.html',
                {'response': 'error'},)


@require_POST
@login_required
@customer_required
def create_order_reorder_khalti(request, order_id, token, coupon=''):
    if coupon:
        coupon_code = Coupon.objects.get(code__iexact = coupon)
        try:
            CouponUsed.objects.get(coupon=coupon_code, customer=request.user.customer)
            return render(request,
                'orders/created.html',
                {'response': 'coupon_already_used'},)
        except Exception:
            pass
    old_order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    form = CreateOrderForm(request,data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        delivery_location = DeliveryLocation.objects.get(id=cd['delivery_location'])

        foods = []
        for item in old_order.items.all():
            foods.append(item.food)
        if not ordered_food_and_restaurant_available(foods):
            return render(request,
                'orders/created.html',
                {'response': 'not_available'})
            
        if not ordered_restaurant_open(foods):
            return render(request,
                'orders/created.html',
                {'response': 'restaurant_close'})

        order = Order.objects.create(customer=request.user.customer, verified=True, delivery_location=delivery_location, transaction=token)
        if coupon:
            order.coupon = Coupon.objects.get(code__iexact = coupon)
            order.save()
            CouponUsed.objects.create(coupon=order.coupon, customer=request.user.customer)
        for item in old_order.items.all():
            OrderItem.objects.create(order=order,
                                    food=item.food,
                                    quantity=item.quantity,
                                    price=item.food.get_selling_price)
        # launch asynchronous task
        order_created_successfully.delay(order.id)
        message = f"Invoice for your order is attached in the pdf file. Your order is verified. You would soon get our delivery person at your door."
        send_invoice.delay(order.id, message)
        order_items = OrderItem.objects.filter(order=order)
        return render(request,
                        'orders/created.html',
                        {'order': order, 'order_items': order_items, 'response': 'success'})
    return render(request,
                'orders/created.html',
                {'response': 'error'},)