from django.contrib import admin
from .models import Brand

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('brand_name',)}
    list_display = ('brand_name','slug')

admin.site.register(Brand,BrandAdmin)
