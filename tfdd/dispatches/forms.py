from django import forms
from models import Follower,Dispatch

class FollowForm(forms.Form):
     phone_number = forms.CharField(max_length=20)
     
class Send_Text(forms.Form):
    to_phone_number = forms.CharField(max_length=20)
    msg_ending=forms.CharField(max_length=50)
    

