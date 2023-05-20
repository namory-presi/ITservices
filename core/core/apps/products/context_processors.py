from .models import *

def categories(request):
    # categorie = CategoryArticle.objects.all().order_by('-id')
    categorie = ''
    return dict(categorie_product=categorie)