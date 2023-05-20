from django.http import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from core.apps.order.models import *
from .models import Cart
from core.apps.products.models import Product
from core.apps.account.models import *
from core.apps.account.forms import *
from core.apps.billing.models import *
from core.apps.addresses.forms import *
from .basket import Basket
from core.apps.order.models import Orders
import json
from core.apps.analytics.signals import *
from core.apps.addresses.forms import AdressForm



def cart(request):
 
    cart, new_obj = Cart.objects.new_or_get(request=request)
    print(f"panier {cart.products.all()}")
    template_name = 'cart/cart.html'
    context = {
        'cart':cart
    }
    return render(request, template_name, context)
    




def cart_update(request):
    print(request.POST)
    product_id = request.POST.get("product_id")

    
    if product_id is not None:
        try:
            obj = Product.objects.get_by_id(id=product_id)
        except Product.DoesNotExist:
            return redirect("cart:main")
        
        cart_obj, new_obj = Cart.objects.new_or_get(request=request)
        if obj in cart_obj.products.all():
            cart_obj.products.remove(obj)
        else:
            cart_obj.products.add(obj)
            
        request.session['cart_items'] = cart_obj.products.count()
        
    return redirect("cart:main")





# @login_required(login_url='account:login')
def chechout_homepage(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request=request)
    order_obj = None
    
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:main")



    login_form = UserLogin()
    guest_form = GuestForm()
    address_form = AdressForm()
    billing_address_form = AdressForm()
    
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request=request)

    
    if billing_profile is not None:
        order_obj, order_obj_created = Orders.objects.new_or_get(billing=billing_profile, cart=cart_obj)
        
    print(f"mes commandes {order_obj} - {cart_obj} ")
    
    template_name = 'cart/checkout.html'
    context = {
        "object": order_obj,
        'cart': cart_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'billing_address_form': billing_address_form
    }
    
    
    return render(request, template_name, context)
    




























# def cart(request):

#     if  request.user.is_authenticated:
#         user = request.user 
#         order, created = Order.objects.get_or_create(customer=user, completed=False)
#         items = order.orderitem_set.all()
#     else:
#         items = []
#         order = {'get_cart_total': 0.00, 'get_cart_items': 0}

#     template_name = 'cart/cart.html'
#     context = {
#         'cart': items,
#         'order': order 
#     }
    
#     return render(request, template_name, context)
    
    




@login_required(login_url='/login')
def checkout(request):
    
    shipping_form = AdressForm(request.POST or None)

    if  request.user.is_authenticated:
        user = request.user 
        order, created = Order.objects.get_or_create(customer=user, completed=False)

        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0.00, 'get_cart_items': 0}

    template_name = 'cart/checkout.html'
    context = {
        'cart': items,
        'order': order,
        'shipping': AdressForm
    }
    
    return render(request, template_name, context)
    
 
 
 
 
 
def updateItem(request):
    
    data = json.loads(request.body)
    productid = data['productId'] 
    action = data['action']
         
    print(f'article {productid}  / action {action}')
    
    customer = request.user 
    product = Product.objects.get_by_id(id=productid)
    order, created = Order.objects.get_or_create(
        customer=customer,
        completed=False
    )
    orderitem, created = OrderItem.objects.get_or_create(
        order=order, 
        product=product
    )
    
    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
        
    orderitem.save()
    
    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse("Article ajouté", safe=False)
