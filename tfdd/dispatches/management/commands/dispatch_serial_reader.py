import logging 

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from serial import Serial

from dispatches.models import RawDispatch


if settings.DEBUG:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)


class Command(BaseCommand):
    help = 'Reads dispatches from the specified serial port'
    def handle(self, *args, **options):
        port = settings.SERIAL_PORT
        baudrate = settings.SERIAL_BAUDRATE
        s = Serial(port, baudrate=baudrate)
        logging.info('listening on %s at %s baud' % (port, baudrate))
        buf = ''
        while 1:
            buf += s.read()
            if 'END OF MESSAGE' in buf:
                raw_dispatch = RawDispatch(text=buf)
                logging.info('received dispatch')
                raw_dispatch.save()
                logging.debug(raw_dispatch.text)
                buf = ''
