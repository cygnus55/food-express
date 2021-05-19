from django import forms
from django.utils.translation import override

FOOD_QUANTITY_CHOICES = [(i, str(i)) for i in range (1,11)]

class CartAddFoodForm(forms.Form):
    quantity = forms.TypedChoiceField(
            choices=FOOD_QUANTITY_CHOICES,
            coerce=int,
        )
    override = forms.BooleanField(required=False, initial=False,
            widget=forms.HiddenInput)