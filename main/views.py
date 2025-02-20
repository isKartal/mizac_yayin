from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def start_test(request):
    return render(request, 'start_test.html')

def more(request):
    return render(request, 'more.html')

def temperaments(request):
    return render(request, 'temperaments.html')