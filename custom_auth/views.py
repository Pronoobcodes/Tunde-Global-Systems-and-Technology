from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Customer
from store.models import Product
from cart.cart import Cart
from .forms import CustomerRegistrationForm, ChangePasswordForm
import json


def register(request):
    form = CustomerRegistrationForm()
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                Customer.objects.create(user=user)
                login(request, user)
                return redirect('update_user') 
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        for error in list(form.errors.values()):
            messages.error(request, error)
    return render(request, 'custom_auth/register.html', {'form': form})


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                login(request, request.user)
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('home') 
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        else:
            form = ChangePasswordForm(user=request.user)
        return render(request, 'custom_auth/change_password.html', {'form': form})
    messages.error(request, 'You need to be logged in to change your password.')
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_profile = Customer.objects.get(user__id=request.user.id)
            saved_cart = user_profile.user_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)

                for key, value in converted_cart.items():
                    try:
                        product = Product.objects.get(id=key)
                        cart.db_add(product=product, quantity=value)
                    except Product.DoesNotExist:
                        continue
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'custom_auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def update_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            address = request.POST.get('address')
            phone = request.POST.get('phone')

            user = request.user
            user.full_name = full_name
            user.address = address
            user.phone = phone
            user.save()

            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('home') 
        return render(request, 'custom_auth/update_user.html', {'user': request.user})
    messages.error(request, 'You need to be logged in to update your profile.')
    return redirect('login')