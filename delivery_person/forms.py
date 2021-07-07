from django import forms

from delivery_person.models import DeliveryPerson


class DeliveryPersonProfileForm(forms.ModelForm):
    class Meta:
        model = DeliveryPerson
        fields = ['full_name', 'profile_pic', 'phone_no']