# from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import restaurant_required
from .models import Category, Restaurant
from accounts.models import User
from .forms import RestaurantRegistrationForm


# Create your views here.


def restaurant_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    # currentTime = datetime.now().time()
    restaurants = Restaurant.objects.all()
    # tmp_restaurant1 = tmp_restaurant.filter(Q(open_hour__lte=F('close_hour')), Q(open_hour__lte=currentTime), close_hour__gte=currentTime)
    # tmp_restaurant2 = tmp_restaurant.filter(available=True).filter(Q(open_hour__gt=F('close_hour')), Q(open_hour__lte=currentTime) | Q(close_hour__gte=currentTime))
    # restaurants = tmp_restaurant1 | tmp_restaurant2
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        restaurants = restaurants.filter(category=category)
    return render(request,
                'restaurants/list.html',
                {'category': category,
                'categories': categories,
                'restaurants': restaurants})


def restaurant_detail(request, id, slug):
    restaurant = get_object_or_404(Restaurant,
                                id=id,
                                slug=slug)
    
    return render(request,
                'restaurants/detail.html',
                {'restaurant': restaurant})



@login_required
@restaurant_required
def restaurant_dashboard(request, username):
    restaurant = Restaurant.objects.get(user__username=username)
    context={
        'restaurant': restaurant,
        'section': 'dashboard',
    }
    return render (request, 'restaurant/dashboard.html',context)


@login_required
@restaurant_required
def update_restaurant_profile(request, username):
    restaurant = Restaurant.objects.get(user__username=username)
    if request.method == 'GET':
        form = RestaurantRegistrationForm(instance=restaurant)
    else:
        form = RestaurantRegistrationForm(data=request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Update Successful')
            return redirect('restaurants:restaurant_dashboard', username=username)

    context={
        'form': form,
        'restaurant': restaurant,
        'section': 'profile',
    }
    return render (request, 'restaurant/profile_update.html',context)