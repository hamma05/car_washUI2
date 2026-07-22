from django.shortcuts import render
from .models import Service


def home(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'home/index.html', {'services': services})


def services_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services/list.html', {'services': services})
