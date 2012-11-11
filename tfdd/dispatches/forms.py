from django import forms
from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USPhoneNumberField

from dispatches.models import EmailVerification, PhoneVerification

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

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('There is already a user with that email.')
        return email

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Passwords do not match.')
        return self.cleaned_data

    def save(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        password = self.cleaned_data['password']
        user = User.objects.create(
            first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        if phone:
            user.profile.phone = phone
            user.profile.save()
            pv = PhoneVerification.create_with_unique_code(phone)
        ev = EmailVerification.create_with_unique_code(email)
        user.save()

class VerifyEmailForm(forms.ModelForm):

    class Meta:
        model = EmailVerification
        fields = ('code',)

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            self.instance = EmailVerification.objects.get(code=code)
        except EmailVerification.DoesNotExist:
            raise ValidationError('Unknown code')
        return code

    def save(self):
        assert self.instance
        email = form.cleaned_data['value']
        self.instance.delete()
        user = User.objects.get(email=email)
        user.profile.email_confirmed = True
        user.profile.save()
        return user

class VerifyPhoneForm(forms.ModelForm):

    class Meta:
        model = PhoneVerification
        fields = ('code',)

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            self.instance = PhoneVerification.objects.get(code=code)
        except PhoneVerification.DoesNotExist:
            raise ValidationError('Unknown code')
        return code

    def save(self):
        assert self.instance
        phone = form.cleaned_data['value']
        self.instance.delete()
        user = User.objects.get(profile__phone=phone)
        user.profile.phone_confirmed = True
        user.profile.save()
        return user

class UpdateSettings(forms.ModelForm):
    phone = USPhoneNumberField(required=False)

    class Meta:
        model = User
        fields =('email',)

    def __init__(self, *args, **kwargs):
        super(UpdateSettings, self).__init__(*args, **kwargs)
        if self.instance:
            self.initial['phone'] = self.instance.profile.phone

    def save(self):
        user = super(UpdateSettings, self).save()
