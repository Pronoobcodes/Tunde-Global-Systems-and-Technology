from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product
from .forms import ProductForm
from custom_auth.models import Customer


# Create your views here.

def admin_view(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    products = Product.objects.all().order_by('id')
    product_form = ProductForm()

    context = {
        'products': products,
        'product_form': product_form,
    }
    return render(request, 'store/admin.html', context)


def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('admin_view')
        else:
            messages.error(request, "Please correct the errors below.")
            products = Product.objects.all().order_by('id')

            return render(request, 'store/product_edit_add.html', {'products': products, 'product_form': form})

    # If GET, show the add-product page with a blank form
    products = Product.objects.all().order_by('id')
    form = ProductForm()
    return render(request, 'store/product_edit_add.html', {'products': products, 'product_form': form})


def edit_product(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('admin_view')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)

    products = Product.objects.all().order_by('id')
    return render(request, 'store/product_edit_add.html', {'form': form, 'product': product, 'products': products})


def delete_product(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect('admin_view')

    return render(request, 'store/confirm_delete.html', {'product': product})


def home(request):
    products = Product.objects.all().order_by('date_added')
    categories = Category.objects.all()
    return render(request, 'store/home.html', {'products': products, 'categories': categories})


def all_products(request):
    search_term = request.GET.get('searched', '')
    sale_filter = request.GET.get('sale')
    sort_order = request.GET.get('sort')
    
    # Start with all products
    products = Product.objects.all()

    # Apply search if provided
    if search_term:
        products = products.filter(
            Q(name__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(category__name__icontains=search_term)
        )

    # Apply sale filter if requested
    if sale_filter == 'true':
        products = products.filter(is_sale=True)

    # Apply sorting
    if sort_order:
        if sort_order == 'low-high':
            products = products.order_by('price')
        elif sort_order == 'high-low':
            products = products.order_by('-price')
        elif sort_order == 'name-az':
            products = products.order_by('name')
        elif sort_order == 'name-za':
            products = products.order_by('-name')
    else:
        # Default sorting by newest
        products = products.order_by('-date_added')

    context = {
        'searched': products,
        'search_term': search_term,
        'sale_filter': sale_filter,
        'sort_order': sort_order,
        'categories': Category.objects.all(),
    }
    
    return render(request, 'store/all_products.html', context)


def sales(request):
    sale_products = Product.objects.filter(is_sale=True)
    return render(request, 'store/sales.html', {'products':sale_products})


def about(request):
    return render(request, 'store/about.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def users_view(request):
    """Admin-only view: list customers with available info."""
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    customers = Customer.objects.all().order_by('id')
    return render(request, 'store/users.html', {'customers': customers})

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).order_by('id')
    return render(request, 'store/category_products.html', {'category': category, 'products': products})
