import datetime
import logging
import random
import requests
import string
import traceback

from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save


class Profile(models.Model):
    """Additional User data"""
    user = models.OneToOneField(User)
    phone = PhoneNumberField()
    phone_confirmed = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "%s's profile" % self.user

    @staticmethod
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(Profile.create_user_profile, sender=User)


class VerificationBase(models.Model):
    code = models.CharField(max_length=6)
    sent_at = models.DateTimeField()

    class Meta:
        abstract = True

    def send(self):
        raise NotImplemented()

    @staticmethod
    def random_code():
        return ''.join(random.sample(string.digits, 6))

    @classmethod
    def create_with_unique_code(cls, value):
        code = cls.random_code()
        while cls.objects.filter(code=code).exists():
            code = cls.random_code()
        obj = cls.objects.create(
            value=value, code=code, sent_at=datetime.datetime.now())
        obj.send()
        return obj


class PhoneVerification(VerificationBase):
    value = PhoneNumberField()

    def send(self):
        from dispatches.twilio_utils import send_msg
        send_msg(self.value, 'Registration code %s' % self.code)


class EmailVerification(VerificationBase):
    value = models.EmailField()

    def send(self):
        send_mail('Registration', 'Registration code %s' % self.code,
            'tfdd@tfdd.com', [self.value], fail_silently=True)


class Station(models.Model):
    """A Fire Station with one or more Units"""
    id = models.CharField(max_length=3, primary_key=True)
    address = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)


class Unit(models.Model):
    """A responder unit or designator"""
    id = models.CharField(max_length=10, primary_key=True)
    station = models.ForeignKey(Station, blank=True, null=True)

    def __unicode__(self):
        return self.id


class UnitFollower(models.Model):
    """A User who wants to be notified of dispatches to a Unit"""
    user = models.ForeignKey(User)
    unit = models.ForeignKey(Unit)
    by_phone = models.BooleanField(
        default=False, help_text='Notify user by phone (SMS)')
    by_email = models.BooleanField(
        default=False, help_text='Notify user by email')


class Dispatch(models.Model):
    call_type = models.CharField(max_length=255)
    call_type_desc = models.CharField('Call type description', max_length=255)
    location = models.CharField(max_length=255)
    dispatched = models.DateTimeField()
    map_page = models.IntegerField()
    notes = models.CharField(blank=True, max_length=255)
    tf = models.IntegerField()
    units = models.ManyToManyField(Unit, related_name='dispatches')

    class Meta:
        verbose_name_plural = 'Dispatches'


class RawDispatch(models.Model):
    dispatch = models.OneToOneField(Dispatch, related_name='raw', blank=True, null=True)
    text = models.TextField()
    received = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(blank=True, null=True)
    
    def parse(self):
        'TODO'

    def post(self):
        url = settings.DISPATCH_POST_URL
        logging.debug('posting raw dispatch to %s' % url)
        try:
            requests.post(url, dict(text=self.text))
        except:
            logging.error(traceback.format_exc())
        else:
            self.sent = datetime.now()
