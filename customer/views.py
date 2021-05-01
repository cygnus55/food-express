from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .decorators import customer_required
from accounts.models import User
from .models import Customer
from .forms import CustomerProfileForm

# Create your views here.

@login_required
@customer_required
def customer_homepage(request):
    return render(request, 'customer/home.html')

@login_required
@customer_required
def cart(request):
    return render(request, 'customer/cart.html')