from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse

from restaurants.decorators import restaurant_required
from .forms import AddRestaurantLocationForm

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


def get_coords_place(request):
    latitude = request.GET.get('latitude', None)
    longitude = request.GET.get('longitude', None)
    geolocator = Nominatim(user_agent='location')
    coords = str(latitude) + ', ' + str(longitude)
    place = geolocator.reverse(coords)
    data = {
        'address': place.address,
    }
    return JsonResponse(data)