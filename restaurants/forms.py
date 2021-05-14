from django import forms

from .models import Restaurant


class RestaurantProfileForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'category', 'name', 'phone_no', 
            'website_link', 'facebook_link', 'logo', 
            'open_hour', 'close_hour', 'description', 'available'
        ]