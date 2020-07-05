from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('cart/',cart),
    re_path(r'cart/(\d+)/',cart_select),
    path('cart/add_cart/',add_cart),
    path('cart/change_select/',select_all),
    path('cart/sub_cart/',sub_cart),
]