from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class Registrationform(UserCreationForm):

    class Meta:
        model=User
        fields=['username', 'email','password1','password2']
