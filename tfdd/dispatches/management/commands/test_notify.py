from django.core.management.base import BaseCommand, CommandError

from dispatches.models import Dispatch


class Command(BaseCommand):
    args = '[tf ...]'
    help = 'Test dispatch notification(s) by tf numbers'


    def handle(self, *args, **options):
        if not len(args) == 1:
            raise CommandError(
                "Need at least one dispatch tf to notify listeners")
        for tf in args:
            dispatch = Dispatch.objects.get(tf=tf)
            dispatch.notify_listeners()
