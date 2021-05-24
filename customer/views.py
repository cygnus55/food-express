from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .decorators import customer_required
from accounts.models import User
from .models import Customer
from .forms import CustomerProfileForm
from foods.models import Food


@login_required
@customer_required
def customer_homepage(request):
    foods = Food.objects.all()
    return render(request, 'customer/home.html', {'foods': foods})


@login_required
@customer_required
def customer_profile_update(request, username):
    customer = Customer.objects.get(user__username=username)
    if request.method == 'GET':
        form = CustomerProfileForm(instance=customer)
    else:
        form = CustomerProfileForm(
            data=request.POST,
            files=request.FILES,
            instance=customer
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile successfully updated!')
            return redirect('customer:profile_update', username=username)
    context = {
        'form': form,
    }
    return render(
        request,
        'customer/profile_update.html',
        context
    )
