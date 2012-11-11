from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
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


class Unit(models.Model):
    id = models.CharField(max_length=10, primary_key=True)

    def __unicode__(self):
        return self.id


class Follower(models.Model):
    phone_number=models.CharField(max_length=20)
    units = models.ManyToManyField(Unit)

    def __unicode__(self):
        return self.phone_number


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
    dispatch = models.OneToOneField(Dispatch, related_name='raw')
    text = models.TextField()
    received = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(blank=True, null=True)
    
    def parse(self):
        'TODO'

    def post(self):
        'TODO' 
