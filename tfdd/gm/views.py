from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
# from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response

from dispatches.models import Dispatch

import urllib2
from django.utils import simplejson as json


@csrf_exempt
def map_redirect(request,tf_number):
    # try:
        map_url="/gm/hydrants?tf_number=%s" % tf_number
        return redirect(map_url)
    # except:
        # return HttpResponseBadRequest()

def hydrant_map(request):
    try:
        tf_number=request.GET.get("tf_number")
        dispatch = Dispatch.objects.get(tf=tf_number)
        return render_to_response(
            'hydrant_map.html', RequestContext(request, 
                dict(dispatch=dispatch)))
    except:
        return HttpResponseBadRequest()
                
def hydrant_heat(request):
    return render_to_response('hydrant_heat.html')

def nearby(request):
    return render_to_response('nearby.html')


def heat_map(request):
    
    dispatches = Dispatch.objects.filter(call_type_desc__contains='FIRE')
    return render_to_response('heat_map.html', RequestContext(request, 
        dict(dispatches=dispatches)))
        