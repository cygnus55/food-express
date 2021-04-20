from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import Category, Restaurant


# Create your views here.


def restaurant_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    currentTime = datetime.now().time()
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


def register_restaurant(request):
    pass