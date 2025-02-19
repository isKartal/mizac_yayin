from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def start_test(request):
    return render(request, 'start_test.html')

def login(request):
    return render(request, 'login.html')

def more(request):
    return render(request, 'more.html')

def temperaments(request):
    return render(request, 'temperaments.html')