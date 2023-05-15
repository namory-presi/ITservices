from django.core.validators import *
from django.utils.safestring import mark_safe
from django.db import models
from django.http import Http404
from django.urls import reverse
from tinymce.models import HTMLField
from django.db.models.signals import *
from djmoney.money import Money
from djmoney.models.fields import MoneyField
from phonenumber_field.phonenumber import PhoneNumber
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from .utils import *
import uuid
import random
import os
from django.db.models import F
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q
from mptt.models import MPTTModel, TreeForeignKey, TreeManager, TreeManyToManyField
from mptt import managers

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f"products/{new_filename}/{final_filename}"




class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
    def search(self, query):
        lookups =( 
                   Q(title__icontains=query) 
                  |Q(description__icontains=query) 
                  |Q(price__icontains=query)
                  |Q(tag__title__icontains=query)
                )
        
        return self.filter(lookups).distinct()


class CategorieQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class CategorieManager(models.Manager):
    
    def get_queryset(self):
        return CategorieQuerySet(self.model, using=self._db)
    

    def all(self):
        return self.get_queryset().active()
    
    
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    
    
    def get_by_slug(self, slug):
        qs = self.get_queryset().active().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None


class ProductManager(models.Manager):
    
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    

    def all(self):
        return self.get_queryset().active()
    
    
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    
    
    def get_by_slug(self, slug):
        qs = self.get_queryset().active().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None
    
    
    def search(self, query):
        return self.get_queryset().active().search(query=query)
    
    

# class CategorieMPTTManager(managers.TreeManager):
#     def get_queryset(self):
#         return CategorieQuerySet(self.model, using=self._db)
    

#     def all(self):
#         return self.get_queryset().active()
    
    
#     def get_by_id(self, id):
#         qs = self.get_queryset().filter(id=id)
#         if qs.count() == 1:
#             return qs.first()
#         return None
    
    
#     def get_by_slug(self, slug):
#         qs = self.get_queryset().active().filter(slug=slug)
#         if qs.count() == 1:
#             return qs.first()
#         return None
    
    
class Category(MPTTModel):
    cat_cku   = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    parent    = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title     = models.CharField(max_length = 150, unique=True, verbose_name='categorie')
    slug      = models.SlugField(max_length=150, unique=True, null=True, blank=True, editable=False)
    active    = models.BooleanField(default=False)
    image     = models.ImageField(upload_to=upload_image_path, blank=True, null=True, height_field=None, width_field=None, max_length=None)
    timestamp = models.DateTimeField("date de creation", auto_now_add=True)
    updated   = models.DateTimeField("date de modification", auto_now=True)
    
    # objects = CategorieMPTTManager()
    
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.cat_cku)
        return super(Category, self).save(*args, **kwargs)

    
    
    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['title']
        verbose_name ='categorie'
        
    def get_absolute_url(self):
         return reverse("products:categorie", kwargs={"slug": self.slug})
    
    
    
    def __str__(self):
        return f'{self.title}'
      
    
class CategoryArticle(models.Model):
    categorie = models.CharField(max_length = 150, unique=True)
    slug      = models.SlugField(max_length=150, unique=True)
    active    = models.BooleanField(default=False)
    image     = models.ImageField(upload_to=upload_image_path, blank=True, null=True, height_field=None, width_field=None, max_length=None)
    timestamp = models.DateTimeField("date de creation", auto_now_add=True)
    updated   = models.DateTimeField("date de modification", auto_now=True)
    
    objects = CategorieManager()
    
    class Meta:
        verbose_name = 'categorie'
        verbose_name_plural = 'categories'
        
          
        
    def get_absolute_url(self):
        return reverse("shop:product_by_categorie", kwargs={"categorie_slug": self.slug})
    
    
    
    def __str__(self):
        return f'{self.categorie}'
    
      
class Product(models.Model):
    category   = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='categorie', related_name='products', null=True, blank=True)
    # categories  = models.ForeignKey(CategoryArticle, verbose_name="categorie", on_delete=models.CASCADE, null=True, blank=True)
    cku         = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    reference   = models.CharField(max_length=10, unique=True, editable=False)
    title       = models.CharField(max_length = 150, unique=True, verbose_name='Article')
    slug        = models.SlugField(max_length=50, unique=True, blank=True, null=True, editable=False)
    overview    = models.CharField(max_length=180, help_text='petite description de l\'article', default='')
    description = HTMLField()
    price       = models.DecimalField(
        max_digits=20,
        decimal_places=2, 
        verbose_name='prix', 
        validators=[
            MaxValueValidator(1000000000000),
            MinValueValidator(100)
        ]
    )
    image       = models.ImageField(upload_to=upload_image_path)
    is_active   = models.BooleanField(default=True, verbose_name='Disponible ?')
    in_stock    = models.BooleanField("En stock ?", default=True)
    timestamp   = models.DateTimeField(auto_now_add=True, verbose_name='date ajout')
    
    
    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})
    
    
    @property
    def categorie(self):
        if self.category:
            return self.category.title
        return ''
    
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.cku)
        if not self.reference:
            self.reference = random_string_generator().upper()
        return super(Product, self).save(*args, **kwargs)
    
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        
        
    objects = ProductManager()
    
    @property
    def related(self):
        try:
            if self.category:
                return self.category.products.all().exclude(pk=self.pk)
        except Product.DoesNotExist:
            raise Http404("Aucun article trouvé !")
        return None
    
    
    @staticmethod
    def get_all_product_by_categories(categorie_slug):
        if categorie_slug:
            return Product.objects.filter(categories__slug=categorie_slug)
        else:
            return Product.objects.all()


    def __str__(self):
        return f'{self.title}'
    
    


# def product_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = random_string_generator()
        
        

# pre_save.connect(product_pre_save_receiver, sender=Product)