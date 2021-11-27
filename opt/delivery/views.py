from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse

from datetime import datetime as dt

from .models import Bus, BusStop, CarryBus
from .serializer import BusSerializer, CarryBusSerializer


# 区間内の駅の名前と時間を全て抽出する
def obtain_all_staions(bus_id, start_station, end_station):
    staion_query = BusStop.objects.filter(bus=bus_id)
    
    station_data = []
    flag = -1
    for staion in staion_query:
        # 初めの駅だったらflagを1にする
        if staion.name == start_station:
            flag *= -1

        # flagが1なら駅の情報を追加する
        if flag == 1:
            tmp = {
                "name": staion.name,
                "time": staion.time.strftime("%Y-%m-%d %H:%M")
            }
            station_data.append(tmp)

        # 最後の駅だっtらflagを-1にする
        if staion.name == end_station:
            flag *= -1

    return station_data


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


@api_view(['GET'])
def obtain_carriable_bus(request):
    if not CarryBus.objects.exclude(max_size=0).exists():
        return JsonResponse({"message": "not found"}, status=400)
    
    carriable_bus_query = CarryBus.objects.exclude(max_size=0)
    bus_data = []
    for carriable_bus in carriable_bus_query:
        tmp = {
            "name": carriable_bus.bus.name,
            # 区間内のすべての駅の名前、時間の配列
            "station": obtain_all_staions(
                carriable_bus.bus.id, carriable_bus.start_station, carriable_bus.end_station)
        }
        bus_data.append(tmp)
    
    return JsonResponse({"bus": bus_data}, status=201)