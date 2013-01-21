from django.core.urlresolvers import reverse
from django.test import TestCase
import mox

from .models import Dispatch, RawDispatch

RAW_DISPATCH_EXAMPLE = (
    u'  \r\r\r\r\r\r\r\r\r\r\r           '
    u'\x07\x07\x07\x07\x07\x07\x07                   '
    u'DISPATCH INFO \r\rCALL TYPE FLUIDS   (ANY TYPE FLUID SPILL)\r'
    u'LOC 7675 E 51 ST S ;KUM-N-GO/10 GALS OR LESS/GASOLINE    \r'
    u'MP 1378 \rDATE 12/10/12 DIS 210421\rUNIT E25    \r     '
    u'TF   2012053706\r \rEND OF MESSAGE')


class PostRawDispatchTest(TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.mox.StubOutWithMock(RawDispatch, 'parse')

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_post_raw_dispatch_empty(self):
        self.mox.ReplayAll()
        response = self.client.post(reverse('dispatches_post_raw'), {})
        self.mox.VerifyAll()
        self.assertEqual(response.status_code, 400)

    def test_post_raw_dispatch(self):
        RawDispatch.parse()
        self.mox.ReplayAll()
        response = self.client.post(reverse('dispatches_post_raw'),
                                    {'text': 'test'})
        self.mox.VerifyAll()
        self.assertEqual(response.status_code, 202)


class RawDispatchParseTest(TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.mox.StubOutWithMock(Dispatch, 'notify_listeners')

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_parse(self):
        Dispatch.notify_listeners()
        self.mox.ReplayAll()
        raw = RawDispatch(text=RAW_DISPATCH_EXAMPLE)
        raw.parse() 
        self.mox.VerifyAll()
        self.assertTrue(raw.dispatch)
        unit = raw.dispatch.units.get()
        self.assertEqual(unit.id, 'E25')
        #TODO: assertEqual other fields
