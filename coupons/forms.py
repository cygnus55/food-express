from django import forms

from .models import Coupon


class CouponApplyForm(forms.Form):
    code = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Apply Coupon'})
    )
