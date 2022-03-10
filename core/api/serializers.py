import hmac
import hashlib
import binascii
from decouple import config
from rest_framework import serializers

from ..models import Person


class PersonSerializer(serializers.ModelSerializer):
    qrcode = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = "__all__"

    def get_qrcode(self, person):
        ''' 
        Generates a code that will be put inside
        a qrcode that will be verified if the
        qrcode is scanned.
        '''
        key = binascii.unhexlify(config("QRCODE_KEY"))
        return hmac.new(
            key,
            person.national_id.encode(),
            hashlib.sha3_512
        ).hexdigest().upper()
