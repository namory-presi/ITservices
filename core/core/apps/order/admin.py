from django.contrib import admin
from import_export import resources
from .models import *
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionMixin


class OrderResource(resources.ModelResource):
    order_id = Field(column_name="N° de commande")
    # cart = Field(column_name="Panier")
    status = Field(column_name="Status")
    shipping_total = Field(column_name="Frais de livraison")
    total = Field(column_name="Total")
    timestamp = Field(column_name="Date de creation")

    class Meta:
        model = Orders
        fields = ("order_id", "cart", "status", "shipping_total", "total", "timestamp")
        export_order =("order_id", "cart", "status", "shipping_total", "total", "timestamp")

    def dehydrate_order_id(self, obj):
        return obj.order_id

    # def dehydrate_cart(self, obj):
    #     return obj.cart

    def dehydrate_status(self, obj):
        if obj.status == "created":
            return "créée"
        elif obj.status == "paid":
            return "payée"
        elif obj.status == "shipped":
            return "livrée"
        else:
            return "remboursée"

    def dehydrate_shipping_total(self, obj):
        return f"{obj.shipping_total} GNF"
    
    
    def dehydrate_total(self, obj):
        return f"{obj.total} GNF"
    
    
    def dehydrate_timestamp(self, obj):
        return obj.timestamp.strftime('%d-%m-%Y à %H:%M')




@admin.register(Orders)
class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_classes = [OrderResource]
    list_display = ("order_id","billing",  "status", "shipping_total", "total", "timestamp")
    list_display_links = ("order_id",  )
    list_filter = ( "status", "timestamp")
    search_fields = ('order_id', )
    list_editable = ('status', )
    readonly_fields = ("order_id", "total", "timestamp")
    
    
