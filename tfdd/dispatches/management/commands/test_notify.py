from django.core.management.base import BaseCommand, CommandError

from dispatches.utils import send_msg
from dispatches.models import Dispatch



class Command(BaseCommand):
    help = 'Test dispatch notification'
    
    
    def handle(self, *args, **options):
        
        dispatch = Dispatch.objects.get(tf='2012049552') 
        
        dispatch.notify_listeners()
