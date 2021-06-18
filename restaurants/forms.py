from django import forms
from django.core.files.images import get_image_dimensions

from .models import Restaurant


class RestaurantProfileForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'category', 'name', 'phone_no', 
            'website_link', 'facebook_link', 'logo', 
            'open_hour', 'close_hour', 'description', 'available'
        ]
    
    def clean_close_hour(self):
        ''' Validate closing time to be greater than opening time. '''
        open_hour = self.cleaned_data.get('open_hour')
        closed_hour = self.cleaned_data.get('close_hour')

        if open_hour >= closed_hour:
            raise forms.ValidationError('Closing hour should be greater than opening hour!')
        
        return closed_hour

    def clean_logo(self):
        ''' Limit the min-width and min-height of logo. '''
        logo = self.cleaned_data.get('logo')
        
        if logo:
            w, h = get_image_dimensions(logo)
            print(w, h)
            if w < 300:
                raise forms.ValidationError(f'The image is {w} pixel wide! It\'s supposed to be at least 300px wide.')
            if h < 300:
                raise forms.ValidationError(f'The image is {h} pixel high! It\'s supposed to be at least 300px high.')
        
        return logo