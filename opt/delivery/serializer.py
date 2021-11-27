from rest_framework import serializers

from .models import Bus, CarryBus


class BusSerializer(serializers.Serializer):
    class Meta:
        model = Bus
        fields = ['id', 'name']


class CarryBusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarryBus
        fields = ['id', 'bus', 'start_station', 'end_station', 'max_size']