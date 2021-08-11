from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .decorators import customer_required
from .models import Customer
from .forms import CustomerProfileForm
from accounts.models import User
from foods.models import Food
from restaurants.models import Restaurant
from orders.models import *
from fav.models import Favorite


@login_required
@customer_required
def customer_homepage(request):
    fav_foods = Favorite.objects.for_user(request.user, model=Food)
    foods = list(map(lambda x: x.target, fav_foods))
    fav_restaurants = Favorite.objects.for_user(request.user, model=Restaurant)
    restaurants = list(map(lambda x: x.target, fav_restaurants))
    return render(
        request, 
        'customer/home.html', 
        {
            'foods': foods,
            'restaurants': restaurants
        }
    )


@login_required
@customer_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user.customer).order_by('-created')
    context = {}
    for order in orders:
        context[order] = OrderItem.objects.filter(order=order)
    return render(request, 'customer/order_history.html', {'context': context})


@login_required
@customer_required
def customer_profile_update(request):
    if request.method == 'GET':
        form = CustomerProfileForm(instance=request.user.customer)
    else:
        form = CustomerProfileForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user.customer
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile successfully updated!')
            return redirect('customer:profile_update')
    context = {
        'form': form,
    }
    return render(
        request,
        'customer/profile_update.html',
        context
    )


@login_required
@customer_required
def fav_restaurant(request, pk):
    ''' Add restaurant to user's favourite '''

    user = request.user
    restaurant = get_object_or_404(Restaurant, pk=pk)
    try:
        Favorite.objects.get_favorite(user, restaurant)
        messages.warning(request, 'Restaurant already added to favourites!')
        return redirect('customer:homepage')
    except Exception:
        pass
    Favorite.objects.create(user, restaurant)
    messages.success(request, 'Restaurant successfully added to favourites!')
    return redirect('restaurants:restaurant_detail', id=restaurant.id, slug=restaurant.slug)


@login_required
@customer_required
def fav_food(request, pk):
    ''' Add food to user's favourite '''

    _next = request.GET.get('next')
    user = request.user
    food = get_object_or_404(Food, pk=pk)
    try:
        Favorite.objects.get_favorite(user, food)
        messages.warning(request, 'Food already added to favourites!')
        return redirect('customer:homepage')
    except Exception:
        pass
    Favorite.objects.create(user, food)
    messages.success(request, 'Food successfully added to favourites!')
    if _next:
        return redirect(_next)
    return redirect('foods:food_detail', pk=food.id)


@login_required
@customer_required
def unfav_restaurant(request, pk):
    ''' Remove restaurant from user's favourite '''
    
    user = request.user
    restaurant = get_object_or_404(Restaurant, pk=pk)
    fav = Favorite.objects.get_favorite(user, restaurant)
    if not fav:
        messages.error(request, 'No such restaurant in your favourites!')
        return redirect('customer:homepage')
    fav.delete()
    messages.success(request, 'Restaurant successfully removed from favourites!')
    return redirect('restaurants:restaurant_detail', id=restaurant.id, slug=restaurant.slug)


@login_required
@customer_required
def unfav_food(request, pk):
    ''' Remove food from user's favourite '''
    
    _next = request.GET.get('next')
    user = request.user
    food = get_object_or_404(Food, pk=pk)
    fav = Favorite.objects.get_favorite(user, food)
    if not fav:
        messages.error(request, 'No such food in your favourites!')
        return redirect('customer:homepage')
    fav.delete()
    messages.success(request, 'Food successfully removed from favourites!')
    if _next:
        return redirect(_next)
    return redirect('foods:food_detail', pk=food.id)