from datetime import datetime
import logging
import random
import re
import requests
import string
import traceback

import dateutil.parser

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save

from .utils import dispatch_msg, send_msg, update


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
            value=value, code=code, sent_at=datetime.now())
        obj.send()
        return obj


class PhoneVerification(VerificationBase):
    value = PhoneNumberField()

    def send(self):
        send_msg(
            self.value,
            'To verify your phone w/ tfdd.co, please visit %s%s?code=%s .' % (
                settings.BASE_URL, reverse('register_phone'), self.code))


class EmailVerification(VerificationBase):
    value = models.EmailField()

    def send(self):
        send_mail(
            'Registration',
            'To verify your email, please visit %s%s?code=%s .' % (
                settings.BASE_URL, reverse('register_email'), self.code),
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
    users = models.ManyToManyField(
        User, through='UnitFollower', blank=True, null=True)

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
    MEDICAL_CALL_TYPES = ('ME', 'MEM', 'MEP', 'CARDIAC')

    class Meta:
        verbose_name_plural = 'Dispatches'

    def notify_listeners(self):
        phones = set()
        emails = set()
        for unit in self.units.all():
            for unitfollower in unit.unitfollower_set.all():
                if unitfollower.by_phone and (
                        unitfollower.user.profile.phone_confirmed):
                    phones.add(unitfollower.user.profile.phone)
                if unitfollower.by_email and (
                        unitfollower.user.profile.email_confirmed):
                    emails.add(unitfollower.user.email)
        for phone in phones:
            if phone:
                send_msg(phone, None, dispatch=self)
        email_msg = dispatch_msg(self)
        for email in emails:
            send_mail(
                'TFD Dispatch %s' % self.call_type_desc,
                email_msg, 'tfdd@tfdd.co', [email], fail_silently=True)


class RawDispatch(models.Model):
    dispatch = models.OneToOneField(Dispatch, related_name='raw', blank=True,
                                    null=True)
    text = models.TextField()
    received = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(blank=True, null=True)
    regex = re.compile(
        r'.*DISPATCH INFO\s+CALL TYPE\s+(?P<call_type>.+)\s+'
        r'\((?P<call_type_desc>.*)\s*\)\s+'
        r'LOC\s+(?P<location>.+)\s+MP\s+(?P<map_page>.+)\s+'
        r'DATE\s+(?P<date>\d+/\d+/\d+)\s+DIS\s+(?P<time>\d+)\s+'
        r'UNIT\s+(?P<units>.+)\s+TF\s+(?P<tf>\d+)\s+END OF MESSAGE', re.S)

    def parse(self):
        match = self.regex.match(self.text)
        if not match:
            self.save()
            logging.error('regex match failure: ' + self.text)
            return
        p = match.groupdict()
        if ';' in p['location']:
            p['location'], p['notes'] = p['location'].split(';', 1)
        for k, v in p.items():
            p[k] = v.strip()
        p['dispatched'] = dateutil.parser.parse(
            p.pop('date') + ' ' + p.pop('time'))
        units = []
        for id in p.pop('units').split():
            unit, created = Unit.objects.get_or_create(id=id)
            units.append(unit)
        self.dispatch, created = Dispatch.objects.get_or_create(**p)
        if created or not self._default_manager.filter(
                dispatch=self.dispatch).exists():
            self.save()
        self.dispatch.units.add(*units)
        if created:
            self.dispatch.notify_listeners()

    def post(self):
        url = settings.DISPATCH_POST_URL
        logging.debug('posting raw dispatch to %s' % url)
        try:
            response = requests.post(url, dict(text=self.text))
        except:
            logging.error(traceback.format_exc())
        else:
            if response.status_code == 202:
                update(self, sent=datetime.now())
            else:
                logging.error('status code %s from server' %
                              response.status_code)
                logging.error(response.content)
