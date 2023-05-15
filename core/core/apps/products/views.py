from django.db import models
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import (ListView, DetailView, DeleteView, CreateView, UpdateView)
from core.apps.marketing.forms import EmailForm
from core.apps.marketing.models import Newsletter
from core.apps.marketing.views import subscribe
# from core.apps.cart.models import Cart
from .models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from mailchimp_marketing import Client
from django.views.decorators.csrf import csrf_exempt


class ProductListView(ListView):
    model = Product
    form_class = EmailForm
    template_name = 'layout/index.html'
    
 
    def get_queryset(self, *args, **kwargs):
        request = self.request
        categories = Category.objects.all().filter(active=True)
        print(categories.count())
        return Product.objects.all()
    
    # def get(self, request, *args, **kwargs):
    #     form = self.form_class
    #     return render(request, 'layout/index.html', {'form': form})

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         new_contact = Newsletter.objects.create(
    #             **form.cleaned_data
    #         )

    #         new_contact.save()
    #         subscribe(new_contact)

    #         messages.success(request, "Merci de votre souscription à notre boite aux lettres ! ") # message
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
    #         return HttpResponseRedirect(reverse('/'))
    #     else:
    #         return render(request, self.template_name, {'form': form})
        
    
    
    
class ProductDetailView(DetailView):
    # qs = Product.objects.all()
    
    template_name = 'layout/detail.html'
    context_object_name = 'detail'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, *args, **kwargs):
        request = self.request
        context = super(ProductDetailView, self).get_context_data(*args,**kwargs)
        # cart_obj, new_obj = Cart.objects.new_or_get(request)
        # context["cart"] = cart_obj
        try:
            context['related_products'] = self.get_object().related
        except AttributeError:
            raise Http404("Aucun article trouvé !")
        return context
        
    
    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get_by_slug(slug)
        except Product.DoesNotExist:
            raise Http404("Aucun article trouvé !")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Cet article n'existe pas !!!")
        return instance
    
    
    
  
  
  
  

@csrf_exempt
def handle404(request, exception):
    
    template_name = 'include/404.html'
    context = {}
    return render(request, template_name, context)
    
  
  






@csrf_exempt
def shop(request):
    categories = None
    products = Product.objects.all().order_by('-id')
    categories = Category.objects.all().filter(active=True)
        
        
    context = {
        'categories': categories,
        'products': products,
    }
    
    template_name = 'layout/shop.html'
    
    return render(request, template_name, context)

    
  

    
    
@csrf_exempt
def categorie_products(request, id, categorie_slug):
    categories = Category.objects.all().filter(active=True)
    products = Product.objects.all().filter(category__id=id, category__slug=categorie_slug)
        
    template_name = 'layout/shop.html'
    context = {
        'categories': categories,
        'products': products,
    }
    
    
    return render(request, template_name, context)
    