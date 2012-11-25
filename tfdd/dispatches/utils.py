import logging
import traceback

from django.conf import settings
from django.core.mail import mail_admins
from django.db.models.expressions import ExpressionNode

from twilio.rest import TwilioRestClient
from twilio.rest.resources import TwilioRestException


def dispatch_msg(dsp):
    unit_msg = "Unit"
    unit_plur = " "
    if dsp.units.count() > 1:
        unit_plur = "s "
    unit_msg = unit_msg + unit_plur
    unit_msg = ' '.join([str(u) for u in dsp.units.all()])
    message = "%s dispatched to %s for %s " % (
        unit_msg, dsp.location, dsp.call_type_desc)
    return message


def email_traceback(subject='Traceback', msg=''):
    exc = traceback.format_exc()
    logging.debug(exc)
    mail_admins(subject, '%s\n%s' % (msg, exc))


def send_msg(to_num, msg_end=None, dispatch=None):
    dispatch_text = ''
    if dispatch:
        dispatch_text = dispatch_msg(dispatch)
    if msg_end:
        dispatch_text = "%s %s" % (dispatch_text, msg_end)
    client = TwilioRestClient(settings.TWILIO_ACCOUNT, settings.TWILIO_TOKEN)
    try:
        client.sms.messages.create(
            to=to_num, from_=settings.TWILIO_FROM, body=dispatch_text)
    except TwilioRestException:
        email_traceback()


def update(instance, **kwargs):
    using = kwargs.pop('using', '')
    get_expression_nodes = kwargs.pop('get_expression_nodes', True)
    updated = instance._default_manager.filter(pk=instance.pk).using(
        using).update(**kwargs)
    if not updated:
        logging.error('update %s: %s failed' % (instance, kwargs))
        return
    expression_nodes = []
    for attr, value in kwargs.items():
        if isinstance(value, ExpressionNode):
            expression_nodes.append(attr)
        else:
            setattr(instance, attr, value)
    if get_expression_nodes and expression_nodes:
        values = instance._default_manager.filter(pk=instance.pk).using(
            using).values(*expression_nodes)[0]
        for attr in expression_nodes:
            setattr(instance, attr, values[attr])
    return updated
