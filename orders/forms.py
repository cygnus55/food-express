from django import forms

from location.models import DeliveryLocation

PAYMENT_CHOICES = (
    ('pay-by-cash', 'Payment by cash on delivery'),
    ('pay-by-khalti', 'Payment by Khalti'),
)


class CreateOrderForm(forms.Form):
    delivery_location = forms.ChoiceField(widget=forms.Select())
    payment_method = forms.ChoiceField(choices = PAYMENT_CHOICES)

    def __init__(self, request, *args, **kwargs):
         super(forms.Form, self).__init__(*args, **kwargs)
         self.fields['delivery_location'].choices = [(l.id, l.title) for l in DeliveryLocation.objects.filter(customer=request.user.customer)]