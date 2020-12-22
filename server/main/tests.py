from django.test import TestCase, Client
from model_mommy import mommy

from main.models import Masternode


class MnAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_create_mn(self):
        self.assertEqual(Masternode.objects.count(), 0)
        r = self.client.put('/api/masternode/', data={"ip": "127.0.0.1", "address": "asdasd", "balance": 222, "pastelID": "asdasd"},
                            content_type='application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Masternode.objects.count(), 1)
        self.assertEqual(Masternode.objects.first().ip, '127.0.0.1')

    def test_update_mn(self):
        mn = mommy.make(Masternode)
        self.assertEqual(Masternode.objects.count(), 1)
        r = self.client.put('/api/masternode/', data={"ip": mn.ip, "address": "NEW ADDR", "balance": 999, "pastelID": "asdasd"},
                            content_type='application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Masternode.objects.count(), 1)
        mn = Masternode.objects.first()
        self.assertEqual(mn.address, 'NEW ADDR')

    def test_no_ip(self):
        mommy.make(Masternode)
        self.assertEqual(Masternode.objects.count(), 1)
        r = self.client.put('/api/masternode/', data={"address": "NEW ADDR", "balance": 999},
                            content_type='application/json')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(Masternode.objects.count(), 1)
        mn = Masternode.objects.first()
        self.assertNotEqual(mn.address, 'NEW ADDR')

    def test_no_patch(self):
        r = self.client.patch('/api/masternode/', data={"address": "NEW ADDR", "balance": 999},
                              content_type='application/json')
        self.assertEqual(r.status_code, 405)

    def test_no_post(self):
        r = self.client.post('/api/masternode/', data={"address": "NEW ADDR", "balance": 999},
                             content_type='application/json')
        self.assertEqual(r.status_code, 405)

    def test_create_pastelID(self):
        self.assertEqual(Masternode.objects.count(), 0)
        r = self.client.put('/api/masternode/', data={"ip": "127.0.0.1",
                                                      "address": "asdasd",
                                                      "balance": 222,
                                                      "pastelID": "asdasd"},
                            content_type='application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Masternode.objects.count(), 1)
        self.assertEqual(Masternode.objects.first().ip, '127.0.0.1')
        self.assertEqual(Masternode.objects.first().pastelID, 'asdasd')
