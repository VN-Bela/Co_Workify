from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class UserRegistration(forms.ModelForm):
    confirm_password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password", "role"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
             "role": forms.Select(attrs={"class": "form-control"}),
          
        }
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))