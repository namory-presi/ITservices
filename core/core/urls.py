from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (handler400, handler403, handler404, handler500)

urlpatterns = [
    
    path('account/', include('core.apps.account.urls', namespace='accounts')),
    path("upload/", include("core.apps.upload.urls", namespace="upload")),
    path("address/", include("core.apps.addresses.urls", namespace="address")),
    path('contact/', include('core.apps.contact.urls', namespace='contact')),
    path('order/', include('core.apps.order.urls', namespace='order')),
    path('billing/', include("core.apps.billing.urls", namespace="billing")),
    path('marketing/', include('core.apps.marketing.urls', namespace='marketing')),
    path('blog/', include('core.apps.blog.urls', namespace='blog')),
    path('about-us/', include('core.apps.about.urls', namespace='about')),
    path('shop/', include('core.apps.shop.urls', namespace='shop')),
    path('tag/', include('core.apps.tags.urls', namespace='tag')),
    path('cart/', include('core.apps.cart.urls', namespace='cart')),
    path('search/', include('core.apps.search.urls', namespace='search')),
    path('tinymce/', include('tinymce.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path("admin/", admin.site.urls),
    path('', include('core.apps.products.urls', namespace='products')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    
    
admin.site.site_header ='IT-SERVICE'                    # default: "Django Administration"
admin.site.index_title ="Interface d'administration"                 # default: "Site administration"
admin.site.site_title = 'IT-SERVICE'  # default: "Django site admin"



handler404 = "core.apps.products.views.handle404"