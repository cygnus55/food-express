from django import forms
from .models import Customer


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'profile_pic', 'phone_no']