from models import Dispatch


from twilio.rest import TwilioRestClient
from django.conf import settings

client = TwilioRestClient(settings.TWILIO_ACCOUNT, settings.TWILIO_TOKEN)


# class Dispatch(models.Model):
#     call_type = models.CharField(max_length=255)
#     call_type_desc = models.CharField('Call type description', max_length=255)
#     location = models.CharField(max_length=255)
#     dispatched = models.DateTimeField()
#     map_page = models.IntegerField()
#     notes = models.CharField(blank=True, max_length=255)
#     tf = models.IntegerField()
#     units = models.ManyToManyField(Unit, related_name='dispatches')


def dispatch_msg(dsp):
    unit_msg="Unit"
    unit_plur=" "
    if units.len>1:
        unit_plur="s "
        
    unit_msg=unit_msg+unit_plur

    unit_msg = ' '.join(dsp.units)
    
    message = "%s dispatched to %s for %s " % (unit_msg, dsp.location,dsp.call_type_desc)



def send_msg(to_num,msg_end,dispatch):
    dispatch_text=''
    
    if dispatch:
        dispatch_text=dispatch_msg(dispatch)

    if msg_end:
        dispatch_text="%s %s" % (dispatch_text,msg_end)
      
    message = client.sms.messages.create(
        to=to_num, 
        from_="+19185508625",
        body=dispatch_text)

