from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Bu kullanıcı adı zaten kullanılıyor.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Bu e-posta adresi zaten kullanılıyor.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('login')  # Ana sayfaya yönlendirme
        else:
            messages.error(request, "Şifreler uyuşmuyor.")
    
    return render(request, 'accounts/register.html')

from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Ana sayfaya yönlendirme
        else:
            messages.error(request, "Kullanıcı adı veya şifre yanlış.")

    return render(request, 'accounts/login.html')

from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')
