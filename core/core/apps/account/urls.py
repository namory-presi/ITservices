from django.urls import path
from . import views
from django.contrib.auth.views import *
from django.views.generic import *

app_name = 'account'

urlpatterns = [
    path('', views.AccountHomeView.as_view(), name='dashboard'),
    path('', views.account_home_view, name='dashboard'),
    path("login/", views.login_page, name="login"),
    path('login/', RedirectView.as_view(url='/login')),
    path("guest/", views.guest_login_page, name="guest_register_url"),
    path('logout/', views.logout_user, name='logout'),
    path("register/", views.register_page, name="register"),
]
