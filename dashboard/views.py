from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from bookings.models import Booking
from bookings.forms import BookingForm
from services.models import Service
from services.forms import ServiceForm


@staff_member_required
def dashboard_home(request):
    today = timezone.localdate()
    today_bookings = Booking.objects.filter(date=today).exclude(status='cancelled')
    upcoming_bookings = Booking.objects.filter(date__gte=today).exclude(status='cancelled').order_by('-date', '-time')[:10]
    all_bookings = Booking.objects.exclude(status='cancelled')

    stats = {
        'today_count': today_bookings.count(),
        'pending': today_bookings.filter(status='pending').count(),
        'in_progress': today_bookings.filter(status='in_progress').count(),
        'done_today': today_bookings.filter(status='done').count(),
        'total_all_time': all_bookings.filter(status='done').count(),
    }
    return render(request, 'dashboard/home.html', {
        'stats': stats,
        'upcoming_bookings': upcoming_bookings,
    })


@staff_member_required
def manage_bookings(request):
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')

    bookings = Booking.objects.all().order_by('-date', '-time')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    if date_filter:
        bookings = bookings.filter(date=date_filter)

    return render(request, 'dashboard/bookings.html', {
        'bookings': bookings,
        'status_filter': status_filter,
        'date_filter': date_filter,
    })


@staff_member_required
def update_booking_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    new_status = request.POST.get('status')
    if new_status in ['pending', 'in_progress', 'done', 'cancelled']:
        booking.status = new_status
        booking.save()
        messages.success(request, f'Réservation #{pk} mise à jour.')
    return redirect('manage_bookings')


@staff_member_required
def toggle_paid(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.paid = not booking.paid
    booking.save()
    return redirect('manage_bookings')


@staff_member_required
def toggle_confirmed(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.confirmed = not booking.confirmed
    booking.save()
    return redirect('manage_bookings')


@staff_member_required
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, f'Réservation #{pk} modifiée.')
            return redirect('manage_bookings')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'dashboard/edit_booking.html', {'form': form, 'booking': booking})


@staff_member_required
def manage_services(request):
    services = Service.objects.all()
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service ajouté.')
            return redirect('manage_services')
    return render(request, 'dashboard/services.html', {'services': services, 'form': form})


@staff_member_required
def toggle_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.is_active = not service.is_active
    service.save()
    return redirect('manage_services')


@staff_member_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    messages.success(request, 'Service supprimé.')
    return redirect('manage_services')
