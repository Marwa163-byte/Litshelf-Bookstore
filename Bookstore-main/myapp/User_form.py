from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'})
    )
####################################################################
class SignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username'})
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'})
    )

    class Meta:
       model = User
       fields = ['username', 'email', 'password1', 'password2','user_type']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
           model = User
           fields = ['username', 'email', 'address', 'contact_number','u_image']
class shop_ProfileUpdateForm(forms.ModelForm):
    class Meta:
           model = Shop
           fields = ['username', 'shop_email','shop_name', 'address', 'contact_number']

class Sub_LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
