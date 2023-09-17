from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from orders.models import OrderProduct
from django.db.models import Q
from .forms import ReviewRatingForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages



def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().order_by('id')

    paginator = Paginator(products, 15)  # Initialize the paginator after the products are set

    page = request.GET.get('page')
    paged_products = paginator.get_page(page)  # Use the paginator to paginate the products

    product_count = paged_products.paginator.count  # Use paged_products.paginator.count for the total count

    context = {
        'product_count': product_count,
        'products': paged_products,
    }
    return render(request, 'store/store.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-date_created').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
    product_count = products.count()
    context = {'products': products, 'product_count': product_count}
    return render(request, 'store/store.html', context)


def product_detail(request, product_slug, category_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()

    except Exception as e:
        raise e
    try:
        is_ordered = OrderProduct.objects.filter(user=request.user, product_id=product).exists()
    except OrderProduct.DoesNotExist:
        is_ordered = None

    context = {'product': product, 'in_cart': in_cart}
    return render(request, 'store/product_detail.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id)
            form = ReviewRatingForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Your review has been updated!')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()

                messages.success(request, 'Your review has been submitted')
                return redirect(url)