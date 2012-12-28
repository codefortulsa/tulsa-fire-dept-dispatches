from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render_to_response
# from django.template import RequestContext
# from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render_to_response


from dispatches.models import Dispatch

@csrf_exempt
def map_redirect(request,tf_number):
    try:
        dispatch = Dispatch.objects.get(tf=tf_number)
        address=dispatch.location
        google_map_url="http://maps.google.com/maps?t=h&z=20&q="+address+"+Tulsa+OK" 
        return redirect(google_map_url)
    except:
        return HttpResponseBadRequest()
