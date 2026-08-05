from django.urls import path
from . import views

urlpatterns = [
    path('connexion/', views.user_login, name='login'),
    path('deconnexion/', views.user_logout, name='logout'),
]
