import hashlib
from rest_framework import serializers

from ..models import Person


class PersonSerializer(serializers.ModelSerializer):
    qrcode = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = "__all__"

    def get_qrcode(self, person):
        return hashlib.sha3_512(
            person.national_id.encode()
        ).hexdigest()
