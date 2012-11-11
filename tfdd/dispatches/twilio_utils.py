from twilio.rest import TwilioRestClient
from django.conf import settings

client = TwilioRestClient(settings.TWILIO_ACCOUNT, settings.TWILIO_TOKEN)

def dispatch_msg(dsp):
    unit_msg="Unit"
    unit_plur=" "
    if dsp.units.count()>1:
        unit_plur="s "
    unit_msg=unit_msg+unit_plur
    unit_msg = ' '.join([str(u) for u in dsp.units.all()])
    message = "%s dispatched to %s for %s " % (unit_msg, dsp.location,dsp.call_type_desc)
    return message


def send_msg(to_num, msg_end=None, dispatch=None):
    dispatch_text=''

    if dispatch:
        dispatch_text=dispatch_msg(dispatch)

    if msg_end:
        dispatch_text="%s %s" % (dispatch_text,msg_end)

    message = client.sms.messages.create(
        to=to_num, 
        from_="+19185508625",
        body=dispatch_text)

