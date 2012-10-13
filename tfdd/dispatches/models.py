from django.db import models

class Dispatch(models.Model):
    call_type = models.CharField(max_length=255)
    call_type_desc = models.CharField('Call type description', max_length=255)
    location = models.CharField(max_length=255)
    dispatched = models.DateTimeField()
    unit = models.CharField(max_length=255)
    map_page = models.IntegerField()
    notes = models.CharField(blank=True, max_length=255)
    tf = models.IntegerField()
    text = models.TextField()

    class Meta:
        verbose_name_plural = 'Dispatches'

