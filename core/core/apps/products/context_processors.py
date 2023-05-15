from .models import *

def categories(request):
    categorie = CategoryArticle.objects.all().order_by('-id')
    return dict(categorie_product=categorie)