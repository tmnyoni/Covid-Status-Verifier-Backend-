from ..utils import generate_hmac_code
from decouple import config
from rest_framework import serializers

from .. import models


class PersonSerializer(serializers.ModelSerializer):
    qrcode = serializers.SerializerMethodField()

    class Meta:
        model = models.Person
        fields = "__all__"

    def get_qrcode(self, person):
        ''' 
        Generates a code that will be put inside
        a qrcode that will be verified if the
        qrcode is scanned.
        '''
        return generate_hmac_code(person.national_id)


class StakeHoldersSerializer(serializers.Serializer):
    class Meta:
        model = models.StakeHolder
        exclude = "__all__"
