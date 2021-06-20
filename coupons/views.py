from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST


from restaurants.decorators import restaurant_required
from customer.decorators import customer_required
from .models import Coupon, CouponUsed
from cart.cart import Cart
from .forms import CouponApplyForm

@login_required
@customer_required
@require_POST
def coupon_apply(request):
    cart = Cart(request)
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact = code, valid_from__lte=now, valid_to__gte=now, active=True)
            try:
                coupon_used = CouponUsed.objects.get(coupon=coupon, customer=request.user.customer)
                messages.warning(request, "You have already used this code.")
            except CouponUsed.DoesNotExist:
                cart.add_coupon(code)
                messages.success(request, 'Coupon code success!')
        except Coupon.DoesNotExist:
            messages.error(request, 'Coupon code error!')
    return redirect('cart:cart_detail')


@login_required
@customer_required
def coupon_unapply(request):
    cart = Cart(request)
    cart.clear_coupon()
    return redirect('cart:cart_detail')