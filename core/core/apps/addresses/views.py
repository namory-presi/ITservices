from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import LoginView, LogoutView
from core.apps.account.forms import GuestForm
from core.apps.account.models import GuestEmail



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
    
    

# Create your views here.
def checkout_address_create_view(request):
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
            return redirect("cart:checkout")
        # else:
        #     print("Erreur")
    # template_name = 'account/login.html'
    context = {
        "form": form
    }
    return  redirect("cart:checkout")
    # return render(request, template_name, context)
    
    
