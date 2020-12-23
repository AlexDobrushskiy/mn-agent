from django.test import TestCase, Client
from model_mommy import mommy

from main.models import Masternode, Regticket, Chunk


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

class RegticketAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.mn = mommy.make(Masternode)

    def test_create(self):
        masternode_pastelid = self.mn.pastelID
        r = self.client.post('/api/regticket/',
                            data={"artist_pastelid":"alslr",
                                  "status": "0",
                                  "image_hash": "nl",
                                  "masternode_pastelid": masternode_pastelid},
                            content_type='application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Regticket.objects.count(), 1)
        self.assertEqual(Regticket.objects.first().image_hash, 'nl')

    def test_no_masternode_pastelid(self):
        r = self.client.post('/api/regticket/',
                            data={"artist_pastelid":"alslr",
                                  "status": "0",
                                  "image_hash": "nl",
                                  "masternode_pastelid": ""},
                            content_type='application/json')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(Regticket.objects.count(), 0)
        self.assertEqual(r.json(), {'masternode_pastelid': ['This field is required.']})

    def test_no_image_hash(self):
        masternode_pastelid = self.mn.pastelID
        r = self.client.post('/api/regticket/',
                            data={"artist_pastelid":"alslr",
                                  "status": "0",
                                  "image_hash": "",
                                  "masternode_pastelid": masternode_pastelid},
                            content_type='application/json')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(Regticket.objects.count(), 0)
        self.assertEqual(r.json(), {'image_hash': ['This field is required.']})

    def test_no_artist_pastelid(self):
        masternode_pastelid = self.mn.pastelID
        r = self.client.post('/api/regticket/',
                            data={"artist_pastelid": "",
                                  "status": "0",
                                  "image_hash": "nl",
                                  "masternode_pastelid": masternode_pastelid},
                            content_type='application/json')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(Regticket.objects.count(), 0)
        self.assertEqual(r.json(), {'artist_pastelid': ['This field is required.']})

    def test_masternode_does_not_exist(self):
        r = self.client.post('/api/regticket/',
                            data={"artist_pastelid": "alslr",
                                  "status": "0",
                                  "image_hash": "nl",
                                  "masternode_pastelid": "sjdls"},
                            content_type='application/json')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(Regticket.objects.count(), 0)
        self.assertEqual(r.json(), {'masternode_pastelid': ['DoesNotExist']})

    def test_unique_image_hash(self):
        masternode_pastelid = self.mn.pastelID
        self.client.post('/api/regticket/',
                            data={"artist_pastelid": "alslr",
                                  "status": "0",
                                  "image_hash": "nl",
                                  "masternode_pastelid": masternode_pastelid},
                            content_type='application/json')

        r = self.client.post('/api/regticket/',
                            data={"artist_pastelid":"alslsssss",
                                  "status": "0",
                                  "image_hash": "nl",
                                  "masternode_pastelid": masternode_pastelid},
                            content_type='application/json')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(Regticket.objects.count(), 1)
        self.assertEqual(r.json(), {'image_hash': ['Must be unique']})

class ChunkAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.mn = mommy.make(Masternode)

    def test_create(self):
        masternode_pastelid = self.mn.pastelID
        r = self.client.post('/api/chunk/',
                             data={"mn_pastelid": masternode_pastelid,
                                   "chunk_id": "efg",
                                   "image_hash": "hijklmnop",
                                   "indexed": "True",
                                   "confirmed": "True",
                                   "stored": "True"},
                             content_type='application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Chunk.objects.count(), 1)
        self.assertEqual(Chunk.objects.first().mn_pastelid.pastelID, masternode_pastelid)


    def test_unique_chunk_id(self):
        masternode_pastelid = self.mn.pastelID
        self.client.post('/api/chunk/',
                             data={"mn_pastelid": masternode_pastelid,
                                   "chunk_id": "efg",
                                   "image_hash": "hijklmnop",
                                   "indexed": "True",
                                   "confirmed": "True",
                                   "stored": "True"},
                             content_type='application/json')

        r = self.client.post('/api/chunk/',
                             data={"mn_pastelid": masternode_pastelid,
                                   "chunk_id": "efg",
                                   "image_hash": "hijklmnop",
                                   "indexed": "True",
                                   "confirmed": "True",
                                   "stored": "True"},
                             content_type='application/json')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(Chunk.objects.count(), 1)
        self.assertEqual(r.json(), {'chunk_id': ['Must be unique']})

    def test_required_mn_pastelid(self):
        masternode_pastelid = self.mn.pastelID
        r = self.client.post('/api/chunk/',
                             data={"mn_pastelid": masternode_pastelid,
                                   "chunk_id": "",
                                   "image_hash": "hijklmnop",
                                   "indexed": "True",
                                   "confirmed": "True",
                                   "stored": "True"},
                             content_type='application/json')

        self.assertEqual(r.status_code, 400)
        self.assertEqual(Chunk.objects.count(), 0)
        self.assertEqual(r.json(), {'chunk_id': ['This field is required.']})

    def test_not_boolean_indexed(self):
        masternode_pastelid = self.mn.pastelID
        r = self.client.post('/api/chunk/',
                             data={"mn_pastelid": masternode_pastelid,
                                   "chunk_id": "efg",
                                   "image_hash": "hijklmnop",
                                   "indexed": "3",
                                   "confirmed": "True",
                                   "stored": "True"},
                             content_type='application/json')

        self.assertEqual(r.status_code, 400)
        self.assertEqual(Chunk.objects.count(), 0)
        self.assertEqual(r.json(), {'indexed': ["This field must be 'True' or 'False'"]})

    def test_not_exist_pastelID(self):
        r = self.client.post('/api/chunk/',
                             data={"mn_pastelid": "abc",
                                   "chunk_id": "efg",
                                   "image_hash": "hijklmnop",
                                   "indexed": "False",
                                   "confirmed": "True",
                                   "stored": "True"},
                             content_type='application/json')

        self.assertEqual(r.status_code, 400)
        self.assertEqual(Chunk.objects.count(), 0)
        self.assertEqual(r.json(), {'masternode_pastelid': ['DoesNotExist']})
