from rest_framework import generics, serializers
from rest_framework.exceptions import ValidationError

from main.models import Masternode


class MasternodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masternode
        fields = ('ip', 'address', 'balance',)


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
