from rest_framework import serializers

from .models import Baggage, Bus, BusStop, CarryBus


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['id', 'name']


class BusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStop
        fields = ['id', 'name', 'time', 'bus']

class CarryBusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarryBus
        fields = ['id', 'bus', 'start_station', 'end_station', 'max_size']


class Baggageserializer(serializers.ModelSerializer):

    class Meta:
        model = Baggage
        fields = ['id', 'carry_bus', 'ride_flag', 'carry_flag', 'fee']
