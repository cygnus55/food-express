from django import forms

from .models import RestaurantLocation, DeliveryLocation


class AddRestaurantLocationForm(forms.ModelForm):
    class Meta:
        model = RestaurantLocation
        fields = ['latitude', 'longitude', 'address']


class AddDeliveryLocationForm(forms.ModelForm):
    class Meta:
        model = DeliveryLocation
        fields = ['title', 'latitude', 'longitude', 'address']
