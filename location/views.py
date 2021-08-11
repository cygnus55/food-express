from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse

from restaurants.decorators import restaurant_required
from customer.decorators import customer_required
from .forms import AddRestaurantLocationForm, AddDeliveryLocationForm
from .models import DeliveryLocation

# geolocation imports
from geopy.geocoders import Nominatim


# Create your views here.


@login_required
@restaurant_required
def add_restaurant_location(request):
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

@login_required
@customer_required
def add_delivery_location(request):
    redirect_url = request.GET.get('next')
    if request.method == 'POST':
        form = AddDeliveryLocationForm(request.POST)
        if form.is_valid():
            form_ = form.save(commit=False)
            form_.customer = request.user.customer
            form_.save()
            messages.success(request, 'Location sucessfully updated!')
            if redirect_url:
                return redirect(redirect_url)
            return redirect('customer:update_delivery_location', location_id=form_.id)
    else:
        form = AddDeliveryLocationForm()
    
    return render(request,
                'location/delivery_location.html',
                {
                    'form': form,
                })
    

@login_required
@customer_required
def update_delivery_location(request, location_id):
    location = get_object_or_404(DeliveryLocation, id=location_id, customer=request.user.customer)
    if request.method == 'POST':
        form = AddDeliveryLocationForm(request.POST, instance=location)
        if form.is_valid():
            form_ = form.save(commit=False)
            form_.customer = request.user.customer
            form_.save()
            messages.success(request, 'Location sucessfully updated!')
            return redirect('customer:update_delivery_location', location_id=location_id)
        
    else:
        form = AddDeliveryLocationForm(instance=location)
        
    return render(request,
            'location/delivery_location.html',
            {
                'form': form,
                'update': True,
                'location': location,
            })


@login_required
@customer_required
def delete_delivery_location(request, location_id):
    location = get_object_or_404(DeliveryLocation, id=location_id, customer=request.user.customer)
    location.delete()
    return redirect('customer:homepage')