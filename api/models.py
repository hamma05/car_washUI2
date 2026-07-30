from django.db import models
from bookings.models import Booking
from services.models import Service

class bookingsapi (models.Model) :
    name= Booking.customer_name
    date_l = Booking.date
    booked_time =Booking.created_at
    confirmation =Booking.confirmed
    status =Booking.status

    def __str__(self) -> str:
        return self.name
