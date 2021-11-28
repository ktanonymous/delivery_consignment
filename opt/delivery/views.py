from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse

from datetime import datetime as dt

from .models import Bus, BusStop, CarryBus
from .serializer import Baggageserializer, BusSerializer, CarryBusSerializer, BusStopSerializer


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

# 駅名、時間から時刻表のクエリを抽出


def obtain_busstop(station, time):
    if not BusStop.objects.filter(name=station, time=time).exists():
        return 0

    time_table = BusStop.objects.get(name=station, time=time)
    return time_table


@csrf_exempt
@api_view(['POST'])
def set_time_table(request):
    serializer = BusStopSerializer(data={
        "name": request.data["name"],
        "time": request.data["time"],
        "bus": request.data["bus_id"],
    })
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['POST'])
def register_bus(request):
    start_station = request.data['start_station']
    end_station = request.data['end_station']
    start_time = request.data['start_time']
    end_time = request.data['end_time']

    # 最初の駅のクエリをとる
    start_time_table = obtain_busstop(start_station, start_time)
    if not start_time_table:
        return JsonResponse({"message": "not found"}, status=400)
    # 最後の駅のクエリをとる
    end_time_table = obtain_busstop(end_station, end_time)
    if not end_time_table:
        return JsonResponse({"message": "not found"}, status=400)

    serializer = CarryBusSerializer(data={
        "bus": start_time_table.bus.id,
        "start_station": start_time_table.id,
        "end_station": end_time_table.id,
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
        bus_company_name = Bus.objects.get(id=carriable_bus.start_station.bus_id)
        tmp = {
            "name": bus_company_name.name,
            # 区間内のすべての駅の名前、時間の配列
            "station": obtain_all_staions(
                carriable_bus.start_station.bus_id,
                carriable_bus.start_station.name,
                carriable_bus.end_station.name
            ),
            "max_size": carriable_bus.max_size,
        }
        bus_data.append(tmp)

    return JsonResponse({"bus": bus_data}, status=201)


@api_view(['POST'])
@csrf_exempt
def reserve_bus(request):
    bus_id = request.data['bus_id']
    try:
        carry_bus = CarryBus.objects.get(bus=bus_id)
    except CarryBus.DoesNotExist:
        resp = {'message': 'invalid bus id is requested'}
        return JsonResponse(resp, status=404)

    size = request.data['size']
    if size > carry_bus.max_size:
        resp = {'message': 'over max size'}
        return JsonResponse(resp, status=404)

    start_station = request.data['start_station']
    end_station = request.data['end_station']

    # NOTE: 配送区間外の場合は無視？？？
    time = request.data['time']
    start_time = dt.strptime(time, '%Y-%m-%d %H:%M:%S%z')
    carry_bus_stops = BusStop.objects.filter(name=end_station,
                                             time__gt=start_time, bus=bus_id)
    end_time = carry_bus_stops.order_by('time').first().time
    fee = size * ((end_time - start_time).seconds // 60)

    baggage = {
        'carry_bus': carry_bus.id,
        'ride_flag': False,
        'carry_flag': False,
        'fee': fee,
    }
    serializer = Baggageserializer(data=baggage)
    if serializer.is_valid():
        serializer.save()

        data = {
            'bus_id': bus_id,
            'start_station': start_station,
            'baggage_id': request.data['baggage_id'],
            'time': time,
        }
        return JsonResponse(data, status=201)
    return JsonResponse(serializer.errors, status=400)
