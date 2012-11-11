from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST

from dispatches.forms import FollowForm
from dispatches.models import Dispatch, Unit


def index(request):
    dispatches = Dispatch.objects.order_by('-dispatched')[:10]
    return render_to_response('index.html', {'dispatches': dispatches})


def follow_unit(request, unit_id):
    assert unit_id
    unit, created = Unit.objects.get_or_create(id=unit_id)
    if request.method == 'POST':
        #form = FollowForm(request.POST)
        #if form.is_valid():
        #    phone = form.cleaned_data['phone_number']
        #    follower, created = Follower.objects.get_or_create(
        #        phone_number=phone)
        #    follower.units.add(unit)
            return redirect('responses_index') # Redirect after POST
    else:
        form = FollowForm() # An unbound form

    c = RequestContext(request, {
        'form': form, 'unit': unit_id
    })

    return render_to_response('follow.html', c)


def register(request):
    if request.user.is_authenticated():
        return redirect('responses_index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('responses_index')
    else:
        assert request.method == 'GET'
        form = RegisterForm(request.GET)
    return render_to_response(
        'register.html', RequestContext(request, {'form': form}))


class HttpResponseAccepted(HttpResponse):
    status = 202


@require_POST
def post(request):
    raw_dispatch = RawDispatch(text=request.POST.get('text'))
    if raw_dispatch.text:
        raw_dispatch.parse()
        raw_dispatch.save()
        return HttpResponseAccepted()
    else:
        return HttpResponseBadRequest()
