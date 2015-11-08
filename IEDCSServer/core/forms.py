from django import forms
from django.forms import ModelForm
from .models import User


# class registerUserForm(forms.Form):
#     username = forms.CharField(label="Username", max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}),)
#     password = forms.CharField(widget=forms.PasswordInput(), required=True,)
#     email = forms.EmailField(label="Email", max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}),)
#     first_name = forms.CharField(label="First Name", max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}),)
#     last_name = forms.CharField(label="Last Name", max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),)


class registerUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'firstName', 'lastName',]
