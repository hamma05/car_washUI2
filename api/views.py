from django.shortcuts import render
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bookings.models import Booking
from .serializer import BookingsSerializer


@api_view(["GET"])
def get_bookings(request) :
    bookings = Booking.objects.all()
    serializer =BookingsSerializer (bookings, many =True)
    return Response(serializer.data)

def get_maps_data(request):
    city = request.GET.get('city', 'New York')
    api_key = 'YOUR_API_KEY'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return JsonResponse(response.json())