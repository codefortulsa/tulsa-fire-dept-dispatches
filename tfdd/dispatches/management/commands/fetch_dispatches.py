import dateutil.parser
import logging 
import requests
 
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import simplejson

from dispatches.models import Dispatch, Unit


if settings.DEBUG:
    LOGLEVEL = logging.DEBUG
else:
    LOGLEVEL = logging.INFO

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=LOGLEVEL)


class Command(BaseCommand):
    help = 'Fetch from https://www.cityoftulsa.org/content/open-data.aspx feed'
    def handle(self, *args, **options):
        resp = requests.get('https://www.cityoftulsa.org/cot/opendata/TFD_dispatch.jsn')
        data = simplejson.loads(resp.content)
        for incident in data['Incidents']['Incident']:
            dispatched = dateutil.parser.parse(incident['ResponseDate'])
            dispatch, created = Dispatch.objects.get_or_create(
                location=incident['Address'],
                call_type=incident['Problem'],
                dispatched=dispatched,
                # FIXME: CoT data has no map_page nor tf
                map_page=1,
                tf=1
            )
            if created:
                dispatch.save()
            units = []
            if type(incident['Vehicles']['Vehicle']) == list:
                for vehicle in incident['Vehicles']['Vehicle']:
                    unit, created = Unit.objects.get_or_create(id=vehicle['VehicleID'])
                    units.append(unit)
            else:
                vehicle = incident['Vehicles']['Vehicle']
                unit, created = Unit.objects.get_or_create(id=vehicle['VehicleID'])
            dispatch.units.add(*units)
            if created:
                dispatch.notify_listeners()
