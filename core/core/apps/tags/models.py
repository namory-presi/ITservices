from django.db import models
from django.urls import reverse
from django.db.models.signals import *
from core.apps.products.models import *
from core.apps.products.utils import *



class Tag(models.Model):
    title      = models.CharField(max_length = 150, unique=True, verbose_name='titre')
    slug       = models.SlugField(max_length=150, unique=True)
    timestamp  = models.DateTimeField(auto_now_add=True)
    products   = models.ManyToManyField(Product, verbose_name="articles", blank=True)
    active     = models.BooleanField("activé ?", default=True)
    
    
    def __str__(self):
        return self.title
    
    
    


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        

pre_save.connect(tag_pre_save_receiver, sender=Tag)
    
    
    
    
    