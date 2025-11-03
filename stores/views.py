from django.shortcuts import render, get_object_or_404
from carts.models import CartItem
from carts.views import _cart_id
from django.db.models import Q
from category.models import Category
from .models import Products
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wishlist.models import Wishlist

def store(request, category_slug=None):
    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Products.objects.filter(category=category, is_available=True)
    else:
        products = Products.objects.filter(is_available=True)

    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    keyword = request.GET.get('keyword')
    if keyword:
        products = products.filter(
            Q(product_name__icontains=keyword) | Q(description__icontains=keyword)
        )

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    elif min_price:
        products = products.filter(price__gte=min_price)
    elif max_price:
        products = products.filter(price__lte=max_price)

    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()
    categories = Category.objects.all()

    context = {
        'products': paged_products,
        'category': categories,
        'product_count': product_count,
        'wishlist_items': wishlist_items, 
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Products.objects.get(category__slug = category_slug, slug = product_slug)
        in_cart        = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=single_product).exists()
        
    except Exception as e :
        raise e
    
    context={
        'single_product' : single_product,
        'in_cart' : in_cart,
    }
    
    return render(request,'store/product_detail.html',context)

def search(request):
    categories = Category.objects.all()
    products = Products.objects.all().order_by('-created_date')
    keyword = request.GET.get('keyword')
    if keyword:
        products = products.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    elif min_price:
        products = products.filter(price__gte=min_price)
    elif max_price:
        products = products.filter(price__lte=max_price)

    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'category': categories,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
