from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.exceptions import ValidationError

from main.models import Masternode


class MasternodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masternode
        fields = ('ip', 'address', 'balance', 'pastelID')

# class RegticketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Regticket
#         fields = ('masternode_pastelid', 'artist_pastelid', 'image_hash', 'status')


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

# class RegticketApiView(generics.UpdateAPIView):
#     serializer_class = RegticketSerializer
#     http_method_names = ['post']
#
#     def get_object(self):
#         pastelID = self.request.data.get('masternode_pastelid')
#         if not pastelID:
#             raise ValidationError({'pastelID': ["This field is required."]})
#         obj, created = Regticket.objects.get_or_create(masternode_pastelid=pastelID)
#         return obj

def show_masternode_data(request):
    field_names = [f.name for f in Masternode._meta.get_fields()]
    print(field_names)
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
