from django.shortcuts import render

# Create your views here.

def fire_more(request):
    return render(request, 'fire_more.html')

def water_more(request):
    return render(request, 'water_more.html')

def temperaments(request):
    return render(request, 'temperaments.html')

def air_more(request):
    return render(request, 'air_more.html')

def earth_more(request):
    return render(request, 'earth_more.html')