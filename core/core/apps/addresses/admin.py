from django.contrib import admin
from .models import *


@admin.register(Adresse)
class AdresseAdmin(admin.ModelAdmin):
    list_display = ("billing_profile", )
    search_fields = ("billing_profile", )