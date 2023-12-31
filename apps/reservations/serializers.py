from rest_framework import serializers
from .models import SonsTimes


class SonsTimeSerializers(serializers.ModelSerializer):
    class Meta:
        model = SonsTimes
        fields = '__all__'

