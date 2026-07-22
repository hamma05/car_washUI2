from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard'),
    path('bookings/', views.manage_bookings, name='manage_bookings'),
    path('bookings/<int:pk>/status/', views.update_booking_status, name='update_booking_status'),
    path('bookings/<int:pk>/paid/', views.toggle_paid, name='toggle_paid'),
    path('bookings/<int:pk>/confirm/', views.toggle_confirmed, name='toggle_confirmed'),
    path('bookings/<int:pk>/edit/', views.edit_booking, name='edit_booking'),
    path('services/', views.manage_services, name='manage_services'),
    path('services/<int:pk>/toggle/', views.toggle_service, name='toggle_service'),
    path('services/<int:pk>/delete/', views.delete_service, name='delete_service'),
]
