from django import forms
from .models import Chef


class ChefProfileForm(forms.ModelForm):
    class Meta:
        model = Chef
        fields = ['name','phone_no','website_link', 'facebook_link', 'logo','open_hour','close_hour','description','available']