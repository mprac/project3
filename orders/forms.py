from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Address

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password1', 'password2']

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

class EditAddressForm(ModelForm): #delete

    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'zipcode']
    
    
