from datetime import datetime
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_any import any_model
from django_any.contrib import any_user
import mox

from dispatches import models



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
        self.mox.StubOutWithMock(models.RawDispatch, 'parse')

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_post_raw_dispatch_empty(self):
        self.mox.ReplayAll()
        response = self.client.post(reverse('dispatches_post_raw'), {})
        self.mox.VerifyAll()
        self.assertEqual(response.status_code, 400)

    def test_post_raw_dispatch(self):
        models.RawDispatch.parse()
        self.mox.ReplayAll()
        response = self.client.post(reverse('dispatches_post_raw'),
                                    {'text': 'test'})
        self.mox.VerifyAll()
        self.assertEqual(response.status_code, 202)


class RawDispatchParseTest(TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.mox.StubOutWithMock(models.Dispatch, 'notify_listeners')

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_parse(self):
        models.Dispatch.notify_listeners()
        self.mox.ReplayAll()
        raw = models.RawDispatch(text=RAW_DISPATCH_EXAMPLE)
        raw.parse() 
        self.mox.VerifyAll()
        dispatch = raw.dispatch
        self.assertTrue(dispatch)
        self.assertEqual(dispatch.call_type, 'FLUIDS')
        self.assertEqual(dispatch.call_type_desc , 'ANY TYPE FLUID SPILL')
        self.assertEqual(dispatch.location, '7675 E 51 ST S')
        self.assertEqual(dispatch.notes, 'KUM-N-GO/10 GALS OR LESS/GASOLINE')
        self.assertEqual(int(dispatch.map_page), 1378)
        self.assertEqual(dispatch.dispatched,
                         datetime(2012, 12, 10, 21, 4, 21))
        self.assertEqual(int(dispatch.tf), 2012053706)
        unit = dispatch.units.get()
        self.assertEqual(unit.id, 'E25')


class NotifyListenersTest(TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.mox.StubOutWithMock(models, 'send_msg')

    def tearDown(self):
        self.mox.UnsetStubs()

    def setup_unit_and_followers(self):
        self.unit = models.Unit.objects.create(id='E25')

        self.phone_follower = any_user(id=1, email='phone@follower.co')
        models.update(self.phone_follower.profile, phone='phone_follower #')
        models.UnitFollower.objects.create(
            unit=self.unit, user=self.phone_follower, by_phone=True)

        self.email_follower = any_user(id=2, email='email@follower.co')
        models.update(self.email_follower.profile, phone='email_follower #')
        models.UnitFollower.objects.create(
            unit=self.unit, user=self.email_follower, by_email=True)

        self.both_follower = any_user(id=3, email='both@follower.co')
        models.update(self.both_follower.profile, phone='both_follower #')
        models.UnitFollower.objects.create(
            unit=self.unit, user=self.both_follower,
            by_email=True, by_phone=True)

        self.neither_follower = any_user(id=4, email='neither@follower.co')
        models.update(self.neither_follower.profile, phone='neither_follower #')
        models.UnitFollower.objects.create(
            unit=self.unit, user=self.neither_follower,
            by_email=False, by_phone=False)

    def test_notify_listeners(self):
        self.setup_unit_and_followers()
        dispatch = any_model(models.Dispatch)
        dispatch.units.add(self.unit)
        models.send_msg('phone_follower #', None, dispatch=dispatch)
        models.send_msg('both_follower #', None, dispatch=dispatch)
        self.mox.ReplayAll()
        dispatch.notify_listeners()
        self.mox.VerifyAll()
        self.assertEqual(len(mail.outbox), 2)
        m0, m1 = mail.outbox
        # can't guarantee order due to use of set
        self.assertTrue(
            m0.to == ['email@follower.co'] and m1.to == ['both@follower.co'] or
            m1.to == ['email@follower.co'] and m0.to == ['both@follower.co'])
