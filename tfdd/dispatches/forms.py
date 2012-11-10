from django import forms
from models import Follower

class FollowForm(forms.Form):
     phone_number = forms.CharField(max_length=20)

