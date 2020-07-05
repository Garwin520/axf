from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('home/',home),
    path('foodtype/',food_type),
    path('market/',market),
]