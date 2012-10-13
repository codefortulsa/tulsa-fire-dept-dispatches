from django.db import models


class Unit(models.Model):
    id = models.CharField(max_length=10, primary_key=True)


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
