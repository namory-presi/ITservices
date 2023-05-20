from django.db import models
import math
from django.db.models.query import QuerySet
from django.urls import reverse
from core.apps.cart.models import Cart
from django.db.models.signals import *
from core.apps.products.models import Product
from core.apps.addresses.models import Adresse
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


ORDER_STATUS_COMPLETED = (
    ("creer", "en cours"),
    ("livrer", "livrée"),
    ("payer", "payer"),
    ("rembourser", "remboursée"),
    ("annuler", "annulée")
)

class OrderManagerQuerySet(models.query.QuerySet):
    
    def recent(self):
        return self.order_by('-date_ordered', '-updated')
    
    
    def by_status(self, status="livrer"):
        return self.filter(status=status)
    

    
    def not_refunded(self):
        return self.exclude(status='rembourser')
    
    
    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request=request)
        return self.filter(billing=billing_profile)
    
    def not_created(self):
        return self.exclude(status='creer')
    
    def new_or_get(self, billing, status):
        created = False
        qs = self.get_queryset().filter(
            billing=billing,
            status='creer'
        )
        
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing=billing
            )
            created = True
        return obj, created
    
    
    
    
   
    

class OrderManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return OrderManagerQuerySet(self.model, using=self._db)
    
    
    
    def recent(self):
        return self.get_queryset().recent()
    
    
    
    def by_request(self, request):
        return self.get_queryset().by_request(request)
    
    
    
    
    def new_or_get(self, billing, cart):
        created = False
        qs = self.get_queryset().filter(billing=billing, cart=cart)
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing=billing, cart=cart)
            created = True
        
        return obj, created
            





class Orders(models.Model):
    billing        = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name='client')
    order_id       = models.CharField(max_length = 150, verbose_name='N° commande', blank=True)
    # shipping_address = models.ForeignKey(Adresse, on_delete=models.CASCADE, verbose_name='adresse livraison', related_name='shipping', null=True, blank=True)
    # billing_address  = models.ForeignKey(Adresse, on_delete=models.CASCADE, verbose_name='adresse de facturation', related_name='billing', null=True, blank=True)
    shipping_address        = models.ForeignKey(Adresse, on_delete=models.CASCADE, blank=True, null=True)
    cart           = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='panier')
    status         = models.CharField(max_length = 150, choices=ORDER_STATUS, default="created")
    shipping_total = models.DecimalField(max_digits=100, decimal_places=2, default=9.99, verbose_name="frais de livraison")
    total          = models.DecimalField(max_digits=100, decimal_places=2, default=0.00, verbose_name="total")
    timestamp      = models.DateTimeField(verbose_name="date de creation", default=now)
    active         = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ("-id", )
        
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
        return f'{self.billing}'



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
        
        

post_save.connect(post_save_cart_total, sender=Cart)
post_save.connect(post_save_order, sender=Orders)
pre_save.connect(pre_save_create_order_id, sender=Orders)


# class Order(models.Model):
#     # billing_profile = models.ForeignKey(BillingProfile, verbose_name="facturation", on_delete=models.CASCADE, null=True, blank=True)
#     customer       = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='client')
#     date_ordered   = models.DateTimeField(auto_now_add=True, verbose_name='date de commande')
#     completed      = models.BooleanField(verbose_name='commande effectuée ?', default=False, null=True, blank=False)
#     status         = models.CharField(max_length = 150, default="creer", choices=ORDER_STATUS_COMPLETED)
#     transaction_id = models.CharField(max_length = 150, null=True, blank=True, verbose_name='N° transaction')
#     updated        = models.DateTimeField(auto_now=True, verbose_name='dernière modification')
      
    
#     class Meta:
#         ordering = ('-id', )
#         verbose_name = 'Panier'
#         verbose_name_plural = 'Paniers'
        
#     @property
#     def get_status(self):
#         if self.status == "creer":
#             return "En cours"
#         elif self.status == "payer":
#             return "Payée"
#         elif self.status == "livrer":
#             return "Livraison en cours"
#         elif self.status == "rembourser":
#             return "Rembourser"
#         else:
#             return "Annuler"
        

        
        
#     def __str__(self):
#         return f'{self.transaction_id}'
    
#     @property
#     def get_cart_total(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([Decimal(item.get_total) for item in orderitems])
#         new_total = Decimal(total)
#         formatted_total = format(new_total, '.2f')
#         return formatted_total
    
    
#     @property
#     def get_cart_items(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.quantity for item in orderitems])
#         return total 
    
#     @property
#     def get_all_items(self):
#         orderitems = self.orderitem_set.all()
#         list_of_item_ordered = [item.product for item in orderitems]
#         return list_of_item_ordered   
 


# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='article')
#     order   = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='N° de commande')
#     quantity = models.IntegerField(verbose_name='quantité', default=0, blank=True, null=True)
#     date_added = models.DateTimeField(verbose_name="date d'ajout", auto_now_add=True)
    
    
#     class Meta:
#         ordering = ('-id', )
#         verbose_name = 'Commande'
#         verbose_name_plural = 'Commandes'
        
        
#     @property
#     def get_total(self):
#         total = Decimal(self.product.price) * Decimal(self.quantity)
#         formatted_total = format(total, '.2f')
#         return formatted_total

#     def __str__(self):
#         return f'{self.product} x ({self.quantity}) '

#     def get_absolute_url(self):
#         return reverse("OrderItem_detail", kwargs={"pk": self.pk})






# def pre_save_cart_receiver(sender, instance, *args, **kwargs):
#     if not instance.transaction_id:
#         instance.transaction_id = random_string_generator().upper()
#         instance.status = 'creer'
    





# pre_save.connect(pre_save_cart_receiver, sender=Order)