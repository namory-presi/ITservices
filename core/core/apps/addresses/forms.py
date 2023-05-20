from django import forms 
from .models import *
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField


class AdressForm(forms.ModelForm):
    
    mobile_phone = PhoneNumberField(label='Telephone', region="GN")
    
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
    
    # state = forms.CharField(label="Region", required=True, widget=forms.TextInput(attrs={
    #     'help_text': "Region/Ville",
    #     "placeholder": "Region/Ville",
    #     "maxlenght": "200"
    # }))
    
    
    city = forms.CharField(label="Ville", required=True, widget=forms.TextInput(attrs={
        'help_text': "Ville",
        "placeholder": "Conakry",
        "maxlenght": "200"
    }))
    
    address = forms.CharField(label='Quartier',required=True,  widget=forms.TextInput(attrs={
        'help_text': 'Nom du quartier',
        'placeholder': 'Nom du quartier',
        'maxlenght': "200"
    }))
    
    street_address = forms.CharField(label='Rue', required=True, widget=forms.TextInput(attrs={
        'help_text': 'Nom de la rue',
        'placeholder': 'Nom de la rue',
        'maxlenght': "200"
    }))
    
    
    message = forms.CharField(widget=forms.Textarea(attrs={'name':'message', 'rows':'10', 'cols':'20', 'placeholder': 'Laisser une note au marchand'}))
    
    
    class Meta:
        model = Adresse
        fields =[
            'lastname',
            'firstname',
            'mobile_phone',
            'country',
            'city',
            'address',
            'street_address',
            'message'
            
        ]
        
        # widgets = {"country": CountrySelectWidget()}
        
        
