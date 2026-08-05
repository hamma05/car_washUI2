from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin-portal/', admin.site.urls),
    path('', include('services.urls')),         # Home page lives in services
    path('accounts/', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/',include('api.urls')),
    path ('',TemplateView.as_view(template_name ='index.html'))
]
