from time import sleep

from django.core.management.base import BaseCommand, CommandError
from serial import Serial


examples = [
'''
                                DISPATCH INFO
CALL TYPE MEM         (EMSA - MONITOR TEL    )
LOC 2000 S 108 E AVE ; CP
    MP 1475
DATE 10/05/12 DIS 125152
UNIT E27
    TF    2012043691

END OF MESSAGE
''',
'''
                                DISPATCH INFO
CALL TYPE MVA         (INJURY VEH ACCIDENT  )
LOC 2700 S SHERIDAN RD
    MP 1326
DATE 10/05/12 DIS 125729
UNIT E21
    TF    2012043692

END OF MESSAGE
''',
'''

                                DISPATCH INFO
CALL TYPE LIFT        (LIFTING ASSISTANCE  )
LOC 4504 E 111 ST S
    MP 1285
DATE 10/05/12 DIS 130730
UNIT E9
    TF    2012043693

END OF MESSAGE
''',
'''
                                DISPATCH INFO
CALL TYPE LIFT        (LIFTING ASSISTANCE  )
LOC 4504 E 111 ST S
    MP 1285
DATE 10/05/12 DIS 130730
UNIT E9     L32
    TF    2012043693

END OF MESSAGE
''',
'''
                                DISPATCH INFO
CALL TYPE MVA         (INJURY VEH ACCIDENT  )
LOC 4600 E 11 ST S ; MC INVOLVED
    MP 1275
DATE 10/05/12 DIS 134322
UNIT E15
    TF    2012043698

END OF MESSAGE
''']


class Command(BaseCommand):
    args = ('port=/dev/ttyUSB0, baudrate=1200, bytesize=8, parity=\'N\', '
            'stopbits=1, timeout=None, xonxoff=False, rtscts=False, '
            'writeTimeout=None, dsrdtr=False, interCharTimeout=None')
    help = 'Reads dispatches from the specified serial port'

    def handle(self, *args, **options):
        options.setdefault('port', '/dev/ttyUSB0')
        options.setdefault('baudrate', 1200)
        s = Serial(*args, **options)
        for dispatch in examples:
            s.write(dispatch)
            sleep(2)
