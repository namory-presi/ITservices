from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from core.apps.order.models import Orders
# from .models import Cart
from core.apps.products.models import Product
from core.apps.account.models import *
from core.apps.account.forms import *
from core.apps.billing.models import *
from core.apps.addresses.forms import *
from .basket import Basket




def cart(request):
    
    # cart_obj, new_obj = Cart.objects.new_or_get(request=request)
    
    template_name = 'cart/cart.html'
    context = {
        'cart': cart_obj
    }
    
    return render(request, template_name, context)
    
    


def cart_update(request):
    product_id = request.POST.get('product_id')
    # obj = None
    # if product_id is not None:
    #     try:
    #         obj = Product.objects.get(id=product_id)
    #         cart_obj, new_obj = Cart.objects.new_or_get(request=request)
            
    #     except Product.DoesNotExist:
            
    #         return redirect('cart:main')
        
    #     if obj in cart_obj.products.all():
    #         print(True)
    #         cart_obj.products.remove(obj)
    #     else:
    #         cart_obj.products.add(obj)
        
    #     print(False)
    #     request.session['cart_item'] = cart_obj.products.count()
    #     print(f"quantité: {request.session['cart_item']}")
            
        
    # cart_obj.products.remove(obj)
    
    # return redirect(obj.get_absolute_url())
    # return redirect('cart:main')






def remove_item_in_the_cart(request, product_id):

    if product_id is not None:
        try:
            obj = Product.objects.get(id=product_id)
            # cart_obj, new_obj = Cart.objects.new_or_get(request=request)
            
        except Product.DoesNotExist:
            
            return redirect('cart:main')
        
        # if obj in cart_obj.products.all():
        #     print(True)
        # 
        # cart_obj.products.remove(obj)
        # else:
        #     cart_obj.products.add(obj)
        
        print(False)
        # request.session['cart_item'] = cart_obj.products.count()
        print(f"quantité: {request.session['cart_item']}")
            
        
    # cart_obj.products.remove(obj)
    
    # return redirect(obj.get_absolute_url())
    return redirect('cart:main')





@login_required(login_url="account:login")
def checkout_home(request):
    # cart_obj, cart_created = Cart.objects.new_or_get(request=request)

    order_obj = None
    
    # if cart_created or cart_obj.products.count() == 0:
    #     return redirect("cart:main")

        

    login_form = UserLogin()
    guest_form = GuestForm()
    address_form = AdressForm()
    billing_address_form = AdressForm()
    
    
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request=request)

    
    # if billing_profile is not None:
    #     order_obj = Orders.objects.new_or_get(billing_profile, cart_obj)

    
    
    template_name = 'cart/checkout.html'
    context = {
        "order": order_obj,
        # "products":cart_obj.products.all(),
        "billing_profile":billing_profile,
        'login_form': login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "billing_address_form": billing_address_form
    }
    
    
    return render(request, template_name, context)
    
    
def basket_summary(request):
    basket = Basket(request=request)
    
    template_name = 'cart/cart.html'
    context = {
        'basket': basket
    }
    return render(request, template_name, context)
    
    
    

def basket_add(request):
    basket = Basket(request=request)
    if request.POST.get('action') == 'post':
        
        product_id = int(request.POST.get('productid'))
        qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        
        basket.add(product=product, qty=qty)
        
        basket_qty = basket.__len__()
        
        response = JsonResponse({
            'product': product_id,
            'qty':basket_qty,
        })
        return response