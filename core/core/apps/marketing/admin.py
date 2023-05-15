from django.contrib import admin
from .models import *

@admin.register(Newsletter)
class NewletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'timestamp')
    