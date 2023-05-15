from typing import Any, Optional
from django.db import models
from django.shortcuts import redirect, render, HttpResponse
from .forms import *
from .models import *
from django.views.generic import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url='account:login')
def account_home_view(request):
    template_name = 'account/account.html'
    context = {}
    return render(request, template_name, context)
    
    
class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'account/account.html'
    def get_object(self):
        return self.request.user



def register_page(request):
    if request.user.is_authenticated:
        return redirect('products:main')

    form = UserRegister(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email    = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        confirm_password = form.cleaned_data.get("confirm_password")
        user  = authenticate(request, username=username,email=email, password=password, confirm_password=confirm_password)
        if user is not None:
            login(request, user)
            return redirect("products:main")
        else:
            print("Erreur")
    template_name = 'account/register.html'
    context = {
        "form": form
    }
    return render(request, template_name, context)
    
    
def guest_login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    form = GuestForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        email = form.cleaned_data.get("email")
        new_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_email.id
        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
        # else:
        #     print("Erreur")
    # template_name = 'account/login.html'
    context = {
        "form": form
    }
    return  redirect("/register/")
    # return render(request, template_name, context)
    

def login_page(request):
    if request.user.is_authenticated:
        return redirect('products:main')
    
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    form = UserLogin(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user  = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("account:dashboard")
        else:
            print("Erreur")
    template_name = 'account/login.html'
    context = {
        "form": form
    }
    return render(request, template_name, context)
    
    

@login_required(login_url="account:login")
def logout_user(request):
    logout(request)
    return redirect("products:main")
    # template_name = 'layout/index.html'
    # context = {}
    # return render(request, template_name, context)
    