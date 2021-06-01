from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from restaurants.decorators import restaurant_required
from .models import RestaurantLocation
from .forms import AddRestaurantLocationForm
from .utils import get_geolocation, get_your_ip

# geolocation imports
from geopy.geocoders import Nominatim


# Create your views here.


@login_required
@restaurant_required
def add_restaurant_location(request):
    geolocator = Nominatim(user_agent='location')
    if request.method == 'POST':
        try:
            form = AddRestaurantLocationForm(data=request.POST, instance=request.user.restaurant.location)
        except Exception:
            form = AddRestaurantLocationForm(data=request.POST)
        if form.is_valid():
            form_ = form.save(commit=False)
            cd = form.cleaned_data
            location_ = str(cd['latitude']) + ', ' + str(cd['longitude'])
            location = geolocator.reverse(location_)
            form_.place = location.address
            form_.restaurant = request.user.restaurant
            form_.save()
            messages.success(request, 'Location sucessfully updated!')
            return redirect('restaurants:add_location')

    else:
        try:
            form = AddRestaurantLocationForm(instance=request.user.restaurant.location)
        except Exception:
            form = AddRestaurantLocationForm()
    return render(request, 
            'location/restaurant_location.html', 
            {
                'form': form,
                'section': 'location',
            })