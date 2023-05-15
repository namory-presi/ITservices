from django.contrib import admin
from .models import *

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')
    prepopulated_fields = {'slug': ('title', )}