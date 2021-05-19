from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import CartAddFoodForm
from .cart import Cart
from .models import Cart as cart_model, CartItem
from foods.models import Food

# Create your views here.

@require_POST
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
def cart_remove(request, food_id):
    cart = Cart(request)
    food = get_object_or_404(Food,id=food_id)
    cart.remove(food)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    quantity_update_form = CartAddFoodForm()
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'quantity_update_form': quantity_update_form})