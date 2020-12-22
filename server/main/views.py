from datetime import datetime

from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from main.models import Masternode, Regticket


class MasternodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masternode
        fields = ('ip', 'address', 'balance', 'pastelID')

class RegticketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regticket
        fields = ('artist_pastelid', 'image_hash', 'status')


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
        print(self.request.data.get('artist_pastelid'))
        artist_pastelid = self.request.data.get('artist_pastelid')
        if not artist_pastelid:
            raise ValidationError({'artist_pastelid': ["This field is required."]})
        obj, created = Regticket.objects.get_or_create(artist_pastelid=artist_pastelid,
                                                       defaults={'status': '0',
                                                                 'created': datetime.now(),})
        return Response('done')

def show_masternode_data(request):
    field_names = [f.name for f in Masternode._meta.get_fields()]
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
