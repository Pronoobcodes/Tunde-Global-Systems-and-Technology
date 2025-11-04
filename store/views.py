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

    return redirect('admin_view')


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

    return render(request, 'store/product_edit_add.html', {'form': form, 'product': product})


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
    q = request.GET.get('q', '')
    products = Product.objects.all().order_by('date_added')

    if q:
        if q.isdigit():
            products = Product.objects.filter(price__lte=float(q)).order_by('date_added')
        else:
            products = Product.objects.filter(
                Q(name__icontains=q) | Q(description__icontains=q) | Q(category__name__icontains=q)
            ).order_by('date_added')

    categories = Category.objects.all()
    return render(request, 'store/home.html', {'products': products, 'categories': categories})


def about(request):
    return render(request, 'store/about.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).order_by('id')
    return render(request, 'store/category_products.html', {'category': category, 'products': products})

def category_summary(request):
    categories = Category.objects.all()
    category_counts = {category: Product.objects.filter(category=category).count() for category in categories}
    return render(request, 'store/category_summary.html', {'category_counts': category_counts})