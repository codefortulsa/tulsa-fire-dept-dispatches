import logging
import traceback

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from dispatches.forms import FollowForm, RegisterForm, Send_Text, VerifyEmailForm, VerifyPhoneForm
from dispatches.models import Dispatch, RawDispatch, Unit
from twilio_utils import send_msg


def index(request):
    dispatches = Dispatch.objects.order_by('-dispatched')[:10]
    return render_to_response('index.html', RequestContext(request, {'dispatches': dispatches}))


def old_follow_unit(request, unit_id):
    assert unit_id
    unit, created = Unit.objects.get_or_create(id=unit_id)
    if request.method == 'POST':
        #form = FollowForm(request.POST)
        #if form.is_valid():
        #    phone = form.cleaned_data['phone_number']
        #    follower, created = Follower.objects.get_or_create(
        #        phone_number=phone)
        #    follower.units.add(unit)
            return redirect('dispatches')  # Redirect after POST
    else:
        form = FollowForm()  # An unbound form

    c = RequestContext(request, {
        'form': form, 'unit': unit_id
    })

    return render_to_response('follow.html', c)


def send_text(request):
    if request.method == 'POST':
        form = Send_Text(request.POST)
        if form.is_valid():
            this_phone = form.cleaned_data['to_phone_number']
            this_msg = form.cleaned_data.get('msg_ending')
            this_dsp = form.cleaned_data.get('dispatch')
            send_msg(to_num=this_phone, msg_end=this_msg, dispatch=this_dsp)
            return redirect('dispatches')  # Redirect after POST
    else:
        form = Send_Text()
        c = RequestContext(request, {
            'form': form,
        })

        return render_to_response('send_text.html', c)


def register(request):
    if request.user.is_authenticated():
        return redirect('dispatches')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispatches')
    else:
        assert request.method == 'GET'
        form = RegisterForm()
    return render_to_response(
        'register.html', RequestContext(request, {'form': form}))


@csrf_exempt
def register_email(request):
    if 'code' in request.REQUEST:
        form = VerifyEmailForm(request.REQUEST)
        if form.is_valid():
            form.save()
            return redirect('dispatches')
    else:
        form = VerifyEmailForm()
    return render_to_response(
        'register_email.html', RequestContext(request, {'form': form}))


@csrf_exempt
def register_phone(request):
    if 'code' in request.REQUEST:
        form = VerifyPhoneForm(request.REQUEST)
        if form.is_valid():
            user = form.save()
            return redirect('dispatches')
    else:
        form = VerifyPhoneForm()
    return render_to_response(
        'register_phone.html', RequestContext(request, {'form': form}))


def unit_select(request):
    if not request.user.is_authenticated():
        return redirect('responses_index')
    all_units = list(Unit.objects.all())
    for unit in all_units:
        follow_q = unit.unitfollower_set.filter(user=request.user)
        if follow_q.exists():
            follow = follow_q.get()
            unit.by_phone = follow.by_phone
            unit.by_email = follow.by_email
    return render_to_response(
        'unit_selection.html', RequestContext(request, {
            'units': all_units}))


def follow_unit(request, unit_id, channel, state):
    assert channel in ['by_phone', 'by_email']
    assert state in ['on', 'off']
    unit, created = Unit.objects.get_or_create(id=unit_id)
    follower, created = request.user.unitfollower_set.get_or_create(unit=unit)
    setattr(follower, channel, state == 'on')
    follower.save()
    return HttpResponse(
        'User %s is now%sfollowing %s %s' %
        (request.user, ' ' if state == 'on' else ' not ', unit, channel))


@csrf_exempt
@require_POST
def post(request):
    raw_dispatch = RawDispatch(text=request.POST.get('text'))
    if raw_dispatch.text:
        try:
            raw_dispatch.parse()
        except:
            logging.error(traceback.format_exc())
            raw_dispatch.save()
        ACCEPTED = 202
        return HttpResponse(status=ACCEPTED)
    else:
        return HttpResponseBadRequest()
