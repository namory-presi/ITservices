from django.db import models
from django.urls import reverse
# from core.apps.cart.models import Cart
from django.db.models.signals import *
from .utils import *
from django.utils.timezone import now
import math
from decimal import Decimal
from core.apps.billing.models import *


ORDER_STATUS = (
    ("created", "créer"),
    ("paid", "payer"),
    ("shipped", "livrer"),
    ("refunded", "rembourser")
)

class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing=billing_profile, cart=cart_obj, active=True)
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing=billing_profile, cart=cart_obj)
            created = True
        
        return obj
            



class Orders(models.Model):
    billing        = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name='client')
    order_id       = models.CharField(max_length = 150, verbose_name='N° commande', blank=True)
    # cart           = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='panier')
    status         = models.CharField(max_length = 150, choices=ORDER_STATUS, default="created")
    shipping_total = models.DecimalField(max_digits=100, decimal_places=2, default=9.99, verbose_name="frais de livraison")
    total          = models.DecimalField(max_digits=100, decimal_places=2, default=0.00, verbose_name="total")
    timestamp      = models.DateTimeField(verbose_name="date de creation", default=now)
    active         = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        
    objects = OrderManager()
        
    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total

    def __str__(self):
        return self.order_id



def pre_save_create_order_id(sender, instance, *args, **kwargs):
    
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance=instance)
        
    qs = Orders.objects.filter(cart=instance.cart).exclude(billing=instance.billing)
    if qs.exists():
        qs.update(active=False)




def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total 
        cart_id = cart_obj.id 
        qs = Orders.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()
    
    
    
    
    
def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()
        
        

# post_save.connect(post_save_cart_total, sender=Cart)
post_save.connect(post_save_order, sender=Orders)
pre_save.connect(pre_save_create_order_id, sender=Orders)