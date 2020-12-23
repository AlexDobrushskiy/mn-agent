from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from main.models import Masternode, Regticket, Chunk


class MasternodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masternode
        fields = ('ip', 'address', 'balance', 'pastelID')

class RegticketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regticket
        fields = ('artist_pastelid', 'image_hash', 'status', 'created', 'masternode_pastelid')

class ChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chunk
        fields = ("mn_pastelid", "chunk_id", "image_hash", "indexed", "confirmed", "stored")


class MasternodeApiView(generics.UpdateAPIView):
    serializer_class = MasternodeSerializer
    http_method_names = ['put']

    def get_object(self):
        # TODO: validate if client's IP equal to this IP in parameters
        ip = self.request.data.get('ip')
        if not ip:
            raise ValidationError({'ip': ["This field is required."]})
        obj, created = Masternode.objects.get_or_create(ip=ip)
        return obj

class RegticketApiView(generics.UpdateAPIView):
    serializer_class = RegticketSerializer
    http_method_names = ['post']
    def post(self, p):
        artist_pastelid = self.request.data.get('artist_pastelid')
        image_hash = self.request.data.get('image_hash')
        pastelID = self.request.data.get('masternode_pastelid')
        if not artist_pastelid:
            raise ValidationError({'artist_pastelid': ["This field is required."]})

        if not image_hash:
            raise ValidationError({'image_hash': ["This field is required."]})
        if not Regticket.objects.filter(image_hash=image_hash).count() == 0:
            raise ValidationError({'image_hash': ["Must be unique"]})

        if not pastelID:
            raise ValidationError({'masternode_pastelid': ["This field is required."]})
        try:
            masternode = Masternode.objects.get(pastelID=pastelID)
        except ObjectDoesNotExist:
            raise ValidationError({'masternode_pastelid': ["DoesNotExist"]})

        obj, created = Regticket.objects.get_or_create(artist_pastelid=artist_pastelid,
                                                       image_hash=image_hash,
                                                       masternode_pastelid=masternode,
                                                       defaults={'status': '0',
                                                                 'created': datetime.now(),})
        serializer = RegticketSerializer(obj)
        return Response(serializer.data)

class ChunkApiView(generics.UpdateAPIView):
    serializer_class = ChunkSerializer
    http_method_names = ['post']
    def post(self, p):
        fields = ("mn_pastelid", "chunk_id", "image_hash", "indexed", "confirmed", "stored")
        data = {}
        for field in fields:
            data[field] = self.request.data.get(field)
            if not data[field]:
                raise ValidationError({field: ["This field is required."]})

        mn_pastelid = data['mn_pastelid']
        chunk_id = data['chunk_id']
        image_hash = data['image_hash']
        indexed = data['indexed']
        confirmed = data['confirmed']
        stored = data['stored']


        if indexed != "True" and indexed != "False":
            raise ValidationError({'indexed': ["This field must be 'True' or 'False'"]})
        if confirmed != "True" and confirmed != "False":
            raise ValidationError({'confirmed': ["This field must be 'True' or 'False'"]})
        if stored != "True" and stored != "False":
            raise ValidationError({'stored': ["This field must be 'True' or 'False'"]})


        if not Chunk.objects.filter(chunk_id=chunk_id).count() == 0:
            raise ValidationError({'chunk_id': ["Must be unique"]})
        try:
            pastelID = Masternode.objects.get(pastelID=mn_pastelid)
        except ObjectDoesNotExist:
            raise ValidationError({'masternode_pastelid': ["DoesNotExist"]})

        obj, created = Chunk.objects.get_or_create(mn_pastelid=pastelID,
                                                   chunk_id=chunk_id,
                                                   image_hash=image_hash,
                                                   indexed=indexed,
                                                   confirmed=confirmed,
                                                   stored=stored,)
        serializer = ChunkSerializer(obj)
        return Response(serializer.data)

def show_masternode_data(request):
    field_names = ['id', 'ip', 'address', 'balance', 'pastelID']
    masternodes = []
    for mn in Masternode.objects.all():
        line = dict()
        for field in field_names:
                line[field] = getattr(mn, field)
        masternodes.append(line)
    context = {
        'masternodes': masternodes,
        'fields': field_names
    }
    return render(request, 'mn_data.html', context=context)
