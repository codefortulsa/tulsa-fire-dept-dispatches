from django.core.management.base import BaseCommand, CommandError

from dispatches.utils import send_msg

class Command(BaseCommand):
    help = 'Test twilio utils'
    def handle(self, *args, **options):
        send_msg("+0000000000","howdy",None)
