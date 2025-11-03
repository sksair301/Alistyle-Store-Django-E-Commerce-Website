from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from carts.models import Cart, CartItem
from carts.views import _cart_id
from stores.models import Products
from .models import Wishlist

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, "Added to your wishlist!")
    else:
        messages.info(request, "This product is already in your wishlist.")
    return redirect('store')


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.warning(request, "Removed from your wishlist.")
    return redirect('wishlist')


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def move_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to add products to your cart.")
        return redirect('login')

    product = get_object_or_404(Products, id=product_id)

    Wishlist.objects.filter(user=request.user, product=product).delete()

    cart_id = _cart_id(request)
    cart, _ = Cart.objects.get_or_create(cart_id=cart_id)

    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        cart=cart,
        defaults={'quantity': 1},
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f" '{product.product_name}' moved to your cart!")
    return redirect('cart')

def toggle_wishlist(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to manage your wishlist.")
        return redirect('login')

    product = get_object_or_404(Products, id=product_id)

    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)

    if wishlist_item.exists():
        messages.info(request, f"'{product.product_name}' is already in your wishlist.")
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, f"Added '{product.product_name}' to your wishlist!")

    return redirect(request.META.get('HTTP_REFERER', 'store'))
