from django.shortcuts import render
from django.views.generic import ListView, DateDetailView, DetailView
from .models import *
from core.apps.billing.models import *


class OrderListView(ListView):
    model = Orders
    template_name = "order.html"
    
    def get_queryset(self):
        my_profile = BillingProfile.objects.new_or_get(self.request)
        return Orders.objects.filter(billing=my_profile)
    

