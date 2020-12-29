from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from main.models import Masternode, Regticket, Chunk, MNConnection


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


class MNConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MNConnection
        fields = ("masternode_pastelid", "ip", "remote_pastelid", "active")


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


class RegticketApiView(generics.CreateAPIView):
    serializer_class = RegticketSerializer

    def perform_create(self, serializer_class):
        serializer_class.save()


class ChunkApiView(generics.CreateAPIView):
    serializer_class = ChunkSerializer

    def perform_create(self, serializer_class):
        serializer_class.save()


class MNConnectionApiView(generics.CreateAPIView):
    serializer_class = MNConnectionSerializer
    http_method_names = ['post']

    def create_or_update(self, data):
        serializer = self.get_serializer(data=data)
        count = MNConnection.objects.filter(masternode_pastelid=data['masternode_pastelid'],
                                            remote_pastelid=data['remote_pastelid']).count()
        if count == 0:
            # create
            serializer.instance = None
        else:
            # update
            serializer.instance = MNConnection.objects.get(masternode_pastelid=data['masternode_pastelid'],
                                            remote_pastelid=data['remote_pastelid'])

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return serializer.data

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            result = []
            for data in request.data:
                serializer_part = self.create_or_update(data)
                result.append(serializer_part)
        else:
            result = self.create_or_update(request.data)
        return Response(result, status=status.HTTP_200_OK)


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
