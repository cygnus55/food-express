from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import CartAddFoodForm
from .cart import Cart
from foods.models import Food
from customer.decorators import customer_required
from orders.forms import CreateOrderForm
from coupons.forms import CouponApplyForm

# Create your views here.


@require_POST
@login_required
@customer_required
def cart_add(request,food_id):
    cart = Cart(request)
    food = get_object_or_404(Food,id=food_id)
    form = CartAddFoodForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(food=food,
                    quantity=cd['quantity'],
                    override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
@login_required
@customer_required
def cart_remove(request, food_id):
    cart = Cart(request)
    food = get_object_or_404(Food,id=food_id)
    cart.remove(food)
    return redirect('cart:cart_detail')


@login_required
@customer_required
def cart_detail(request):
    cart = Cart(request)
    create_order_form = CreateOrderForm(request)
    coupon_apply_form = CouponApplyForm()
    return render(request,
            'cart/cart_detail.html',
            {
                'cart': cart,
                'create_order_form': create_order_form,
                'coupon_apply_form': coupon_apply_form,
            })
