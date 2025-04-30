from django.shortcuts import render
from testing_algorithm.models import TestResult

def temperaments(request):
    """Tüm mizaçları gösteren genel sayfa"""
    
    # Eğer kullanıcı giriş yapmışsa, kendi mizaç sonucunu da gönderelim
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
        if test_result:
            # Test sonucundan kullanıcının elementini al
            user_element = test_result.dominant_element
            context = {
                'user_element': user_element,
                'has_test_result': True
            }
        else:
            context = {
                'has_test_result': False
            }
    else:
        context = {
            'has_test_result': False
        }
        
    return render(request, 'temperaments/temperaments.html', context)

def fire_more(request):
    """Ateş mizacı detay sayfası"""
    
    # Eğer kullanıcı giriş yapmışsa, kendi mizaç sonucuyla karşılaştırma yapalım
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
        if test_result:
            # Kullanıcının mizacı ile karşılaştır
            is_users_element = test_result.dominant_element.name == "Ateş"
            context = {
                'is_users_element': is_users_element,
                'has_test_result': True
            }
        else:
            context = {
                'has_test_result': False
            }
    else:
        context = {
            'has_test_result': False
        }
        
    return render(request, 'temperaments/fire_more.html', context)

def water_more(request):
    """Su mizacı detay sayfası"""
    
    # Eğer kullanıcı giriş yapmışsa, kendi mizaç sonucuyla karşılaştırma yapalım
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
        if test_result:
            # Kullanıcının mizacı ile karşılaştır
            is_users_element = test_result.dominant_element.name == "Su"
            context = {
                'is_users_element': is_users_element,
                'has_test_result': True
            }
        else:
            context = {
                'has_test_result': False
            }
    else:
        context = {
            'has_test_result': False
        }
        
    return render(request, 'temperaments/water_more.html', context)

def air_more(request):
    """Hava mizacı detay sayfası"""
    
    # Eğer kullanıcı giriş yapmışsa, kendi mizaç sonucuyla karşılaştırma yapalım
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
        if test_result:
            # Kullanıcının mizacı ile karşılaştır
            is_users_element = test_result.dominant_element.name == "Hava"
            context = {
                'is_users_element': is_users_element,
                'has_test_result': True
            }
        else:
            context = {
                'has_test_result': False
            }
    else:
        context = {
            'has_test_result': False
        }
        
    return render(request, 'temperaments/air_more.html', context)

def earth_more(request):
    """Toprak mizacı detay sayfası"""
    
    # Eğer kullanıcı giriş yapmışsa, kendi mizaç sonucuyla karşılaştırma yapalım
    if request.user.is_authenticated:
        test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
        if test_result:
            # Kullanıcının mizacı ile karşılaştır
            is_users_element = test_result.dominant_element.name == "Toprak"
            context = {
                'is_users_element': is_users_element,
                'has_test_result': True
            }
        else:
            context = {
                'has_test_result': False
            }
    else:
        context = {
            'has_test_result': False
        }
        
    return render(request, 'temperaments/earth_more.html', context)