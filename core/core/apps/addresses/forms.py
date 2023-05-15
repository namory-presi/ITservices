from django import forms 
from .models import *
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField
    # billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, verbose_name='client')
    # address_type   = models.CharField(verbose_name="type d'adresse", max_length=50,  choices=ADDRESS_TYPE)
    # lastname       = models.CharField(max_length = 150, verbose_name="nom", blank=True, null=True)
    # firstname       = models.CharField(max_length = 150, verbose_name="prenom", blank=True, null=True)
    # mobile_phone   = PhoneNumberField(blank=True, verbose_name="telephone")
    # country        = CountryField(verbose_name="pays")
    # state          = models.CharField("region", max_length=50, default="Conakry")
    # city           = models.CharField("ville", max_length=50)
    # street_address = models.CharField(max_length = 150, verbose_name="quartier/rue")
    # message        = models.TextField()
    
    

class AdressForm(forms.ModelForm):
    
    lastname = forms.CharField(label="Nom", required=True, widget=forms.TextInput(attrs={
        'help_text': "Nom de famille",
        "placeholder": "Votre nom de famille",
        "maxlenght": "200"
    }))
    firstname = forms.CharField(label="Votre prenom", required=True, widget=forms.TextInput(attrs={
        'help_text': "Prénom",
        "placeholder": "Votre prénom",
        "maxlenght": "200"
    }))
    
    message = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':10, 'cols':30}))
    class Meta:
        model = Adresse
        fields = ("lastname", "firstname", "mobile_phone",  "country", "state", "street_address", "message")
        
        widgets = {"country": CountrySelectWidget()}