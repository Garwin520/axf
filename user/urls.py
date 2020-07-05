from django.urls import path
from .views import *

urlpatterns = [
    path('auth/register/',register),
    path('auth/login/',login),
    path('auth/',user_info),
]