from django.db import models
from stores.models import Products
from category.models import Category

class Cart(models.Model):
    cart_id         = models.CharField(max_length=250, blank=True)
    date_added      = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product         = models.ForeignKey(Products, on_delete=models.CASCADE)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity        = models.IntegerField()
    is_active       = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)
