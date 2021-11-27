from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse

from datetime import datetime as dt

from .models import Bus, BusStop, CarryBus
from .serializer import BusSerializer, CarryBusSerializer


@csrf_exempt
@api_view(['POST'])
def register_bus(request):
    start_station = request.data['start_station']
    time = dt.strptime(request.data['time'], '%Y-%m-%d %H:%M:%S%z')
    if not BusStop.objects.filter(name=start_station, time=time).exists():
        return JsonResponse({"message": "not found"}, status=400)

    time_table = BusStop.objects.get(name=start_station, time=time)
    serializer = CarryBusSerializer(data={
        "bus": time_table.bus.id,
        "start_station": start_station,
        "end_station": request.data['end_station'],
        "max_size": request.data['max_size']
    })
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)
