from django import forms

from location.models import DeliveryLocation
from delivery_person.models import DeliveryPerson 

class CreateOrderForm(forms.Form):
    delivery_location = forms.ChoiceField(widget=forms.Select())

    def __init__(self, request, *args, **kwargs):
         super(forms.Form, self).__init__(*args, **kwargs)
         self.fields['delivery_location'].choices = [(l.id, l.title) for l in DeliveryLocation.objects.filter(customer=request.user.customer)]


class OrderDesignateForm(forms.Form):
    delivery_person = forms.ChoiceField(widget=forms.Select())

    def __init__(self, *args, **kwargs):
         super(forms.Form, self).__init__(*args, **kwargs)
         self.fields['delivery_person'].choices = [(dp.id, dp.full_name) for dp in DeliveryPerson.objects.all()]
