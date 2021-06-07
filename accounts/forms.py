from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}), 
        label='Username/ Email'
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']
        help_texts = {
            'username': '',
            'password1': '',
            'password2': ''
        }