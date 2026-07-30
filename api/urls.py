from django.urls import path
from api import views

urlpatterns =[
    
    path("bookings_api/", views.get_bookings ,name='get_bookings'),
    
]