from django import forms

from location.models import DeliveryLocation

class CreateOrderForm(forms.Form):
    delivery_location = forms.ChoiceField(widget=forms.Select())

    def __init__(self, request, *args, **kwargs):
         super(forms.Form, self).__init__(*args, **kwargs)
         self.fields['delivery_location'].choices = [(l.id, l.title) for l in DeliveryLocation.objects.filter(customer=request.user.customer)]