from django import forms
from django.forms.widgets import TextInput

from .models import RestaurantLocation


class AddRestaurantLocationForm(forms.ModelForm):
    class Meta:
        model = RestaurantLocation
        fields = ['latitude', 'longitude']

    # def __init__(self, *args, **kwargs):
    #     super(AddRestaurantLocationForm, self).__init__(*args, **kwargs)
    #     self.fields['latitude'].widget.attrs['disabled'] = True
    #     self.fields['longitude'].widget.attrs['disabled'] = True
