from django.shortcuts import renderget_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#from .decorators import restaurant_required
from .models import Chef
from accounts.models import User
from .forms import ChefProfileForm


# Create your views here.


def chef_list(request, category_slug=None):
    category = None
    # currentTime = datetime.now().time()
    chefs = Chef.objects.all()
    # tmp_restaurant1 = tmp_restaurant.filter(Q(open_hour__lte=F('close_hour')), Q(open_hour__lte=currentTime), close_hour__gte=currentTime)
    # tmp_restaurant2 = tmp_restaurant.filter(available=True).filter(Q(open_hour__gt=F('close_hour')), Q(open_hour__lte=currentTime) | Q(close_hour__gte=currentTime))
    # restaurants = tmp_restaurant1 | tmp_restaurant2
    #if category_slug:
     #   category = get_object_or_404(Category, slug=category_slug)
     #   chefs = restaurants.filter(category=category)
    return render(request,
                'restaurants/list.html',
                {'category': category,
                'categories': categories,
                'restaurants': restaurants})
