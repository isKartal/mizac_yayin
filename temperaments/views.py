from django.shortcuts import render

# Create your views here.

def fire_more(request):
    return render(request, 'temperaments/fire_more.html')

def water_more(request):
    return render(request, 'temperaments/water_more.html')

def temperaments(request):
    return render(request, 'temperaments/temperaments.html')

def air_more(request):
    return render(request, 'temperaments/air_more.html')

def earth_more(request):
    return render(request, 'temperaments/earth_more.html')