from django.db import models
from django.urls import reverse

class Brand(models.Model):
    brand_name          = models.CharField(max_length=50, unique=True)
    slug                = models.SlugField(max_length=150, unique=True)
    
    def __str__(self):
        return self.brand_name
