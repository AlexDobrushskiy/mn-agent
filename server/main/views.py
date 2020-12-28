from django.shortcuts import render
from rest_framework import generics, serializers
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
        MNConnection.objects.update_or_create(masternode_pastelid=data['masternode_pastelid'],
                                              defaults={'ip': "{}".format(data['ip']),
                                              'active':'{}'.format(data['active']),
                                              'remote_pastelid' :'{}'.format(data['remote_pastelid'])})
        return

    def data_to_list(self, connection_data):
        req_data = {}
        for connection_data_field in connection_data:
            part_req_data = {connection_data_field: connection_data[str(connection_data_field)]}
            if connection_data_field == 'masternode_pastelid':
                part_req_data['masternode_pastelid'] = connection_data['masternode_pastelid'].pastelID
            req_data |= part_req_data
        return req_data

    def post(self, data):
        if str(type(self.request.data)) == "<class 'list'>":
            serializer = self.get_serializer(data=self.request.data, many=isinstance(self.request.data, list))
            serializer.is_valid(raise_exception=True)
            for val_data in serializer.validated_data:
                self.create_or_update(val_data)
            list_req_data = []
            for connection_data in serializer.validated_data:
                req_data = self.data_to_list(connection_data)
                list_req_data.append(req_data)
            return Response(list_req_data)
        else:
            serializer = MNConnectionSerializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            self.create_or_update(serializer.validated_data)
            connection_data = serializer.validated_data
            req_data = self.data_to_list(connection_data)
            return Response(req_data)


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
