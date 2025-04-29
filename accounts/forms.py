from django import forms

from django.core.validators import MaxLengthValidator,MinLengthValidator
# from .models import LoginField,SignupField

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,label="Username")
    password = forms.CharField(max_length=20,widget=forms.PasswordInput,label="Password")


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30,label="First Name")
    last_name = forms.CharField(max_length=30,label="Last Name")
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Username")
    password1 = forms.CharField(widget=forms.PasswordInput,label="Password",validators=[MinLengthValidator(8),MaxLengthValidator(30)])
    password2 = forms.CharField(widget=forms.PasswordInput,label="Confirm Passowrd")