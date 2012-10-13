from django.core.management.base import BaseCommand, CommandError
from serial import Serial

from dispatches.models import RawDispatch

class Command(BaseCommand):
    args = 'port=/dev/ttyUSB0, baudrate=9600, bytesize=8, parity=\'N\', '
           'stopbits=1, timeout=None, xonxoff=False, rtscts=False, '
           'writeTimeout=None, dsrdtr=False, interCharTimeout=None'
    help = 'Reads dispatches from the specified serial port'

    def handle(self, *args, **options):
        options.setdefault('port', '/dev/ttyUSB0')
        s = Serial(*args, **options)
        buf = ''
        while 1:
            buf += s.read()
            if 'END OF MESSAGE' in buf:
                RawDispatch.objects.create(text=buf)
                self.stdout.write(buf)
                buf = ''
