from django.shortcuts import render
from .models import *

def about(request):
    
    about = About.objects.all().first()
    
    template_name = 'layout/about.html'
    context = {
        'about': about
    }
    
    return render(request, template_name, context)
    
    


def faq(request):
    
    about = FAQ.objects.all().order_by("-id")
    
    template_name = 'layout/faq.html'
    context = {
        'faq': faq
    }
    
    return render(request, template_name, context)
    