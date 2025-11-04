from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Customer
from .forms import CustomerRegistrationForm, ChangePasswordForm


def register(request):
    form = CustomerRegistrationForm()
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                Customer.objects.create(user=user)
                login(request, user)
                return redirect('home') 
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        for error in list(form.errors.values()):
            messages.error(request, error)
    return render(request, 'auth/register.html', {'form': form})


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('home') 
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        else:
            form = ChangePasswordForm(user=request.user)
        return render(request, 'auth/change_password.html', {'form': form})
    messages.error(request, 'You need to be logged in to change your password.')
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def update_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')

            user = request.user
            user.full_name = full_name
            user.phone = phone
            user.address = address
            user.save()

            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('home') 
        return render(request, 'auth/update_user.html', {'user': request.user})
    messages.error(request, 'You need to be logged in to update your profile.')
    return redirect('login')