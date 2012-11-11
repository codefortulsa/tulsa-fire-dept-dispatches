from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField


class FollowForm(forms.Form):
     phone_number = forms.CharField(max_length=20)

class Send_Text(forms.Form):
    to_phone_number = forms.CharField(max_length=20)
    msg_ending=forms.CharField(max_length=50)

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = USPhoneNumberField(required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Again', widget=forms.PasswordInput)
