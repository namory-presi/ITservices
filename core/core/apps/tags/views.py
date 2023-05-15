from django.shortcuts import render
from .models import *
from django.views.generic import *

class TagListView(ListView):
    template_name = 'layout/shop.html'
    context_object_name = 'tags'
    
    