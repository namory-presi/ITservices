from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart, name='main'),
    path('update/', cart_update, name="update"),
    path('checkout/', chechout_homepage, name='checkout'),
]
