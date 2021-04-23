from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}))


class Registrationform(UserCreationForm):

    class Meta:
        model=User
        fields=['username', 'email','password1','password2']
