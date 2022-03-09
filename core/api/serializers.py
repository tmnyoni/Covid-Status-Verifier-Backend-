from rest_framework import serializers

from ..models import Person


class PersonSerializer(serializers.Serializer):
    class Meta:
        model = Person
        fields = "__all__"
