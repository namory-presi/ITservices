from django.urls import path
from . import views

app_name ="address"

urlpatterns = [
    path('shipping/create/', views.checkout_address_create_view, name='shipping'),
]
