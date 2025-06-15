from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter first name"
    }))
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter last name"
    }))
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter email"
    }))
    birthday = forms.DateField(widget=forms.DateInput(attrs={
        "class": "form-control",
        "placeholder": "YYYY-MM-DD",
        "type": "date"
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter username"
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Enter password"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm password"
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birthday', 'password1', 'password2']



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter username"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Enter password"
    }))