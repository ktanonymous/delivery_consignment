from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Baggage
from .serializer import Baggageserializer

from rest_framework.decorators import api_view

@csrf_exempt

def check_finish(request):
    carry_query = request.data['baggage_id']
    
    message = Baggage(name='baggage', tagline='carry_flag')
    if carry_query == True:
        message.save()
        return True

    else:
        message.save()
        return False

    return False