from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import login


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'pages/register.html', {'form': form})


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')

def checkout(request):
    return render(request, 'checkout.html')

def cart(request):
    return render(request, 'cart.html')

def confirmation(request):
    return render(request, 'confirmation.html')

def elements(request):
    return render(request, 'elements.html')
