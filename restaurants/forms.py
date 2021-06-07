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
    
    def clean_close_hour(self):
        ''' Validate closing time to be greater than opening time. '''
        open_hour = self.cleaned_data.get('open_hour')
        closed_hour = self.cleaned_data.get('close_hour')

        if open_hour > closed_hour:
            raise forms.ValidationError('Closing hour should be greater than opening hour!')
        
        return closed_hour