from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST


from restaurants.decorators import restaurant_required
from .models import Coupon
from .forms import CouponApplyForm
from .forms import AddCouponForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact = code, valid_from__lte=now, valid_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

    return redirect('cart:cart_detail')



@login_required
@restaurant_required
def add_coupon(request):
    if request.method == 'POST':
        form = AddCouponForm(data=request.POST)
        if form.is_valid():
            form_ = form.save(commit=False)
            form_.restaurant = request.user.restaurant
            form_.save()
            messages.success(request, 'Sucessfully applied!')
            return redirect('restaurants:add_coupon')
    else:
        form = AddCouponForm()
    return render(request, 'coupons/add_coupon.html', {'form': form, 'section': 'coupons'})    

