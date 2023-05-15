from django.contrib import admin
from .models import BillingProfile

@admin.register(BillingProfile)
class BillingProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "active")
    search_fields = ("active", )
    readonly_fields = ("update", "timestamp")