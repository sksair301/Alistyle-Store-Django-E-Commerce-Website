from django.db import models
from django.urls import reverse
from brands.models import Brand
from category.models import Category

class Products(models.Model):
    product_name        = models.CharField(max_length=100, unique=True)
    slug                = models.SlugField(max_length=155, unique=True)
    description         = models.TextField(max_length=255, blank=True)
    price               = models.IntegerField()
    stock               = models.IntegerField()
    images              = models.ImageField(upload_to='photos/products')
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand               = models.ForeignKey(Brand,blank=True, null=True, on_delete=models.CASCADE)
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)
    manufacturer        = models.CharField(max_length=100, blank=True)
    article_number      = models.CharField(max_length=100, blank=True, null=True)
    guarantee           = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name
