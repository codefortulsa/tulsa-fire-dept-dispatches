import logging
import traceback

from django.contrib.auth.views import login as auth_login
from django.contrib.auth.views import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from emailusernames.forms import EmailAuthenticationForm

from .forms import (RegisterForm, VerifyEmailForm, VerifyPhoneForm,
                    UpdateSettings)
from .models import Dispatch, RawDispatch, Unit, UnitFollower


@login_required
def dispatch_list(request, start_tf=0, how_many=10, dispatch_filter={}):

    try:
        dispatch_filter=eval(dispatch_filter)
    except:
        dispatch_filter={}
  
    try:
        start_tf=int(start_tf)
    except:
        start_tf=0
        
    if start_tf==0:
        max_tf=Dispatch.objects.aggregate(Max('tf'))
        dispatch_filter['tf']=max_tf
    else:
        dispatch_filter['tf__lt']=start_tf        
    
    try:            
        dispatches = Dispatch.objects.filter(**dispatch_filter).order_by('-dispatched')[:how_many]
        
        return render_to_response(
            'dispatch_list.html', RequestContext(request, 
                dict(dispatches=dispatches,
                     dispatch_filter=dispatch_filter)))
    except:
        return HttpResponseBadRequest()


@login_required
def check_for_update(request, start_tf=0, dispatch_filter={}):

    try:
        dispatch_filter=eval(dispatch_filter)
    except:
        dispatch_filter={}
  
    try:
        start_tf=int(start_tf)
    except:
        return HttpResponseBadRequest()
        
    update_filter=dispatch_filter.copy()
    update_filter['tf__gt']=start_tf        
    
    # try:            
    dispatches = Dispatch.objects.filter(**update_filter).order_by('-dispatched')

    if dispatches.count() > 0:
        return render_to_response(
            'dispatch_list.html', RequestContext(request, 
                dict(dispatches=dispatches,
                     update_filter=update_filter,
                     dispatch_filter=dispatch_filter)))
    else:
        return HttpResponseBadRequest()

    # except:
    #     return HttpResponseBadRequest()

@login_required
def dispatch_location(request, location_address):
    return render_to_response(
        'dispatch_location.html', RequestContext(request, 
            dict(location_address=location_address)))


def index(request,*args):
    dispatches = Dispatch.objects.order_by('-dispatched')[:10]            
    return render_to_response('index.html', RequestContext(request,
    dict(dispatches=dispatches)))


@login_required
def following(request,):
    dispatch_filter = dict(units__unitfollower__user = request.user.id)
    dispatches = Dispatch.objects.filter(**dispatch_filter).order_by('-dispatched')[:5]
    return render_to_response('following.html', 
        RequestContext(request, 
            dict(dispatches=dispatches,
                 dispatch_filter=dispatch_filter
            )))


@login_required(login_url='/dispatches/login/')
def unit_detail(request,unit_id):
    dispatch_filter = dict(units__id=unit_id)
    dispatches = Dispatch.objects.filter(**dispatch_filter).order_by('-dispatched')[:5]
    followers=UnitFollower.objects.filter(unit=unit_id)

    return render_to_response(
        'unit_dispatches.html', RequestContext(request, 
            {'unit_id':unit_id
            ,'dispatches':dispatches
            ,'followers':followers
            ,'dispatch_filter':dispatch_filter
            }))        


def about(request):
    return render_to_response('about.html')


def login(request):
    return auth_login(
        request, template_name='login.html',
        authentication_form=EmailAuthenticationForm)
        

def logout(request):
    return auth_logout(request, next_page=reverse('dispatches'))


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
            form.save()
            return redirect('dispatches')
    else:
        form = VerifyPhoneForm()
    return render_to_response(
        'register_phone.html', RequestContext(request, {'form': form}))


@login_required
def unit_select(request):
    if not request.user.is_authenticated():
        return redirect('dispatches')
    all_units = list(Unit.objects.order_by('id'))
    for unit in all_units:
        follow_q = unit.unitfollower_set.filter(user=request.user)
        if follow_q.exists():
            follow = follow_q.get()
            unit.by_phone = follow.by_phone
            unit.by_email = follow.by_email
            # remove UnitFollower if no notifications
            if not follow.by_phone and not follow.by_email:
                follow.delete()
    return render_to_response(
        'unit_selection.html', RequestContext(request, {
            'units': all_units}))


@login_required
def follow_unit(request, unit_id, channel, state):
    # TODO: this needs to be rewritten to use the POST method
    if channel not in ['by_phone', 'by_email'] or state not in ['on', 'off']:
        return HttpResponseBadRequest()
    unit, created = Unit.objects.get_or_create(id=unit_id)
    try:
        follower, created = request.user.unitfollower_set.get_or_create(
            unit=unit)
    except UnitFollower.MultipleObjectsReturned:
        unit_followers = request.user.unitfollower_set.all()
        follower = unit_followers[0]
        for uf in unit_followers[1:]:
            uf.delete()
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


@login_required
def update_settings(request):
    if request.method == 'POST':
        form = UpdateSettings(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dispatches')  # Redirect after POST
    else:
        c = RequestContext(
            request, dict(form=UpdateSettings(instance=request.user)))
        return render_to_response('settings.html', c)
