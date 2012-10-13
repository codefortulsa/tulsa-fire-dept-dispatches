from django.shortcuts import render_to_response

from dispatches.models import Dispatch

def index(request):
    dispatches = Dispatch.objects.order_by('-dispatched')[:10]
    return render_to_response('index.html', {'dispatches': dispatches})
