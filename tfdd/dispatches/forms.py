from django import forms

class FollowForm(forms.Form):
    phone_number = forms.CharField(max_length=20)

class RegisterForm(forms.Form):
    pass
