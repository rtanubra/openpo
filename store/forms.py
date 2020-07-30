from django.forms import ModelForm
from .models import *
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type='date'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['seller']
    
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['seller']

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        exclude= ['seller']

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class SellerForm(ModelForm):
    class Meta:
        model = Seller
        fields = '__all__'
        exclude= ['user']
        