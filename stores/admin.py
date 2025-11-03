from django.contrib import admin
from .models import Products

class productAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('product_name',)}
    list_display = ('product_name', 'category', 'price', 'stock', 'manufacturer','modified_date','is_available')

admin.site.register(Products,productAdmin)
