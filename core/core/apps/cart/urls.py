from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('add/', basket_add, name='basket_add'),
    path('', cart, name='main'),
    path('checkout/', checkout_home, name='checkout'),
    path('update/', cart_update, name='update'),
    path('remove/<int:product_id>/', remove_item_in_the_cart, name='remove'),
    
]
