from rest_framework import serializers
from bookings.models import Booking

class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['customer_name', 'date', 'created_at', 'confirmed', 'status']