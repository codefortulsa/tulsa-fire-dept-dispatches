from django.db import models


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
