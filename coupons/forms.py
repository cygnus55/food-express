from django import forms

from .models import Coupon


class CouponApplyForm(forms.Form):
    code = forms.CharField()

class AddCouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'valid_from', 'valid_to', 'discount', 'active']
        help_text = {
            'valid_from': 'Format: YYYY-MM-DD HH:MM',
            'valid_to': 'Format: YYYY-MM-DD HH:MM',
        }
