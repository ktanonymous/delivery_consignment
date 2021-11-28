from django.db import models


class Bus(models.Model):
    name = models.CharField(max_length=255)


class BusStop(models.Model):
    name = models.CharField(max_length=255)
    time = models.DateTimeField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)


class CarryBus(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    start_station = models.ForeignKey(BusStop, related_name='start_station',
                                      on_delete=models.CASCADE)
    end_station = models.ForeignKey(BusStop, related_name='end_station',
                                    on_delete=models.CASCADE)
    max_size = models.IntegerField()


class Baggage(models.Model):
    carry_bus = models.ForeignKey(CarryBus, on_delete=models.CASCADE)
    ride_flag = models.BooleanField()
    carry_flag = models.BooleanField()
    fee = models.IntegerField()
