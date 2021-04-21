from django import forms
from .models import Restaurant


class RestaurantRegistrationForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['category','name','address','logo','open_hour','close_hour','description','available']



    