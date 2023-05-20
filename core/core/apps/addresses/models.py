from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from core.apps.billing.models import BillingProfile
from django_countries.fields import CountryField
from django.conf import settings
from core.apps.order.models import *

User = settings.AUTH_USER_MODEL


ADDRESS_TYPE = (
    ('livraison', "Livraison"),
    ("facturation", "Facturation")
)

class Adresse(models.Model):

    billing_profile = models.OneToOneField(BillingProfile, on_delete=models.CASCADE, verbose_name='client')
    address_type   = models.CharField(max_length = 150, choices=ADDRESS_TYPE)
    lastname       = models.CharField(max_length = 150, verbose_name="nom", blank=True, null=True)
    firstname       = models.CharField(max_length = 150, verbose_name="prenom", blank=True, null=True)
    mobile_phone   = PhoneNumberField(blank=True, verbose_name="telephone")
    country        = models.CharField(verbose_name="pays", default='Guinée', max_length=200)
    city           = models.CharField("ville", max_length=50)
    address        = models.CharField(max_length = 150, verbose_name="adresse")
    street_address = models.CharField(max_length = 150, verbose_name="Rue", blank=True, null=True)
    
    message        = models.TextField(blank=True, null=True)
    
    

    
    def __str__(self):
        return  f'{self.billing_profile}'
    
    
    class Meta:
        verbose_name = "Differente adresse"
        verbose_name_plural = "Differentes adresses"
        ordering = ("-id", )


    def get_absolute_url(self):
        return reverse("Adresse_detail", kwargs={"pk": self.pk})
