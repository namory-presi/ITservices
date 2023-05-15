from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from core.apps.billing.models import BillingProfile
from django_countries.fields import CountryField


ADDRESS_TYPE = (
    ('livraison', "Livraison"),
    ("facturation", "Facturation")
)

class Adresse(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, verbose_name='client')
    address_type   = models.CharField(verbose_name="type d'adresse", max_length=50,  choices=ADDRESS_TYPE)
    lastname       = models.CharField(max_length = 150, verbose_name="nom", blank=True, null=True)
    firstname       = models.CharField(max_length = 150, verbose_name="prenom", blank=True, null=True)
    mobile_phone   = PhoneNumberField(blank=True, verbose_name="telephone")
    country        = CountryField(verbose_name="pays")
    state          = models.CharField("region", max_length=50, default="Conakry")
    city           = models.CharField("ville", max_length=50)
    street_address = models.CharField(max_length = 150, verbose_name="quartier/rue")
    message        = models.TextField()
    
    

    
    def __str__(self):
        return  f'{self.billing_profile}'
    
    
    class Meta:
        verbose_name = "Adresse"
        verbose_name_plural = "Adresses"
        ordering = ("-id", )


    # def get_absolute_url(self):
    #     return reverse("Adresse_detail", kwargs={"pk": self.pk})
