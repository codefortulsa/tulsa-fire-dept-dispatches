from django import forms
from models import Follower

class FollowForm(forms.ModelForm):
    # phone_number = forms.CharField(max_length=20)
    
    class Meta:
        model=Follower
        fields=('phone_number',)