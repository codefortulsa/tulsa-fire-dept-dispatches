from django.shortcuts import render_to_response

from dispatches.models import Dispatch,Follower

from dispatches.forms import FollowForm

from django.template import RequestContext

from django.http import HttpResponseRedirect

def index(request):
    dispatches = Dispatch.objects.order_by('-dispatched')[:10]
    return render_to_response('index.html', {'dispatches': dispatches})
    
def follow_unit(request):
    
    if request.method == 'POST':
        follower, created = get_or_create(Follower, phone)
        form = FollowForm(request.POST) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dispatches') # Redirect after POST
    else:
        form = FollowForm() # An unbound form

    c=RequestContext(request,    {
            'form': form,'unit':request.GET['unit']
        })
    
    return render_to_response('follow.html', c)