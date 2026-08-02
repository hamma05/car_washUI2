import json

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm
from .models import Booking
from services.models import Service


def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            _send_notification(booking)
            messages.success(request, 'R\u00e9servation confirm\u00e9e ! \u00c0 bient\u00f4t.')
            return redirect('booking_confirm', pk=booking.pk)
    else:
        form = BookingForm()

    services = [
        {
            'name': s.name,
            'description': s.description,
            'price': str(s.price),
            'duration_minutes': s.duration_minutes,
        }
        for s in Service.objects.filter(is_active=True)
    ]
    context = {
        'form': form,
        'services_json': json.dumps(services, ensure_ascii=False),
    }
    if form.errors:
        context['form_errors_json'] = json.dumps(form.errors, ensure_ascii=False)
        context['form_data_json'] = json.dumps(
            {k: v for k, v in form.data.items() if k != 'csrfmiddlewaretoken'},
            ensure_ascii=False,
        )
    return render(request, 'bookings/create.html', context)


def _send_notification(booking):
    recipient = settings.RECIPIENT_EMAIL
    if not recipient:
        return

    context = {
        'id': booking.pk,
        'nom': booking.customer_name,
        'telephone': booking.customer_phone,
        'service': booking.service.name if booking.service else '-',
        'date': booking.date,
        'heure': booking.time,
        'notes': booking.notes or '-',
        'status': dict(Booking.STATUS_CHOICES).get(booking.status, booking.status),
        'paye': 'Oui' if booking.paid else 'Non',
        'confirme': 'Oui' if booking.confirmed else 'Non',
    }

    subject = f'[HBIBWASH] Nouvelle reservation #{booking.pk} - {booking.customer_name}'

    text = """Nouvelle reservation #{id}
-------------------------------

Client : {nom}
Telephone : {telephone}
Date : {date}
Heure : {heure}
Notes : {notes}

Statut : {status}
Paye : {paye}
Confirme : {confirme}

Reservation creee le : {cree}
-------------------------------""".format(
        id=context['id'],
        nom=context['nom'],
        telephone=context['telephone'],
        service=context['service'],
        date=context['date'],
        heure=context['heure'],
        notes=context['notes'],
        status=context['status'],
        paye=context['paye'],
        confirme=context['confirme'],
        cree=booking.created_at.strftime('%d/%m/%Y a %H:%M') if booking.created_at else '-',
    )

    html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:'DM Sans',Arial,sans-serif; background:#f5f5f0; padding:2rem;">
<div style="max-width:560px; margin:0 auto; background:white; border-radius:12px; border:1px solid #e0e0d8; overflow:hidden;">
<div style="background:#0a0a0a; padding:1.5rem 2rem;">
<h1 style="font-family:'Bebas Neue',sans-serif; color:#f5f5f0; letter-spacing:2px; font-size:1.8rem; margin:0;">
HBIB<span style="color:#1a6bff;">Wash</span>
</h1>
</div>
<div style="padding:2rem;">
<h2 style="font-size:1.2rem; margin:0 0 1.5rem; color:#0a0a0a;">
Nouvelle r&eacute;servation <span style="color:#1a6bff;">#{id}</span>
</h2>
<table style="width:100%; border-collapse:collapse; font-size:0.9rem;">
<tr><td style="padding:0.6rem 0; color:#6b7280; border-bottom:1px solid #e0e0d8;">Client</td><td style="padding:0.6rem 0; font-weight:600; border-bottom:1px solid #e0e0d8;">{nom}</td></tr>
<tr><td style="padding:0.6rem 0; color:#6b7280; border-bottom:1px solid #e0e0d8;">T&eacute;l&eacute;phone</td><td style="padding:0.6rem 0; font-weight:600; border-bottom:1px solid #e0e0d8;">{telephone}</td></tr>
<tr><td style="padding:0.6rem 0; color:#6b7280; border-bottom:1px solid #e0e0d8;">Date</td><td style="padding:0.6rem 0; font-weight:600; border-bottom:1px solid #e0e0d8;">{date}</td></tr>
<tr><td style="padding:0.6rem 0; color:#6b7280; border-bottom:1px solid #e0e0d8;">Heure</td><td style="padding:0.6rem 0; font-weight:600; border-bottom:1px solid #e0e0d8;">{heure}</td></tr>
<tr><td style="padding:0.6rem 0; color:#6b7280; border-bottom:1px solid #e0e0d8;">Notes</td><td style="padding:0.6rem 0; font-weight:600; border-bottom:1px solid #e0e0d8;">{notes}</td></tr>
<tr><td style="padding:0.6rem 0; color:#6b7280; border-bottom:1px solid #e0e0d8;">Statut</td><td style="padding:0.6rem 0; font-weight:600; border-bottom:1px solid #e0e0d8;">{status}</td></tr>
<tr><td style="padding:0.6rem 0; color:#6b7280; border-bottom:1px solid #e0e0d8;">Pay&eacute;</td><td style="padding:0.6rem 0; font-weight:600; border-bottom:1px solid #e0e0d8;">{paye}</td></tr>
<tr><td style="padding:0.6rem 0; color:#6b7280; border-bottom:1px solid #e0e0d8;">Confirm&eacute;</td><td style="padding:0.6rem 0; font-weight:600; border-bottom:1px solid #e0e0d8;">{confirme}</td></tr>
<tr><td style="padding:0.6rem 0; color:#6b7280;">Cr&eacute;&eacute;e le</td><td style="padding:0.6rem 0; font-weight:600;">{cree}</td></tr>
</table>
</div>
</div>
</body>
</html>""".format(
        id=context['id'],
        nom=context['nom'],
        telephone=context['telephone'],
        service=context['service'],
        date=context['date'],
        heure=context['heure'],
        notes=context['notes'],
        status=context['status'],
        paye=context['paye'],
        confirme=context['confirme'],
        cree=booking.created_at.strftime('%d/%m/%Y &agrave; %H:%M') if booking.created_at else '-',
    )

    send_mail(subject, text, settings.EMAIL_HOST_USER, [recipient], html_message=html)


def booking_confirm(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'bookings/confirm.html', {'booking': booking})

def maps(request):
    return render(request, 'templates/home/index.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })