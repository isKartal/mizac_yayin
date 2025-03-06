from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from testing_algorithm.models import TestResult, ElementType 

@login_required
def profiles(request):
    """ Profil ana sayfasını gösterir """
    return render(request, 'profiles.html')

@login_required
def my_temperament(request):
    """ Kullanıcının en son yaptığı testi ve mizaç sonucunu gösterir """
    test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()

    return render(request, 'my_temperament.html', {
        'result': test_result,
        'dominant_element': test_result.dominant_element if test_result else None,
        'element_scores': {
            'Ateş': test_result.fire_score if test_result else 0,
            'Hava': test_result.air_score if test_result else 0,
            'Su': test_result.water_score if test_result else 0,
            'Toprak': test_result.earth_score if test_result else 0
        } if test_result else None
    })

@login_required
def my_suggestions(request):
    """ Kullanıcının baskın elementiyle ilgili önerileri gösterir """
    test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()

    element = test_result.dominant_element if test_result else None

    return render(request, 'my_suggestions.html', {
        'element': element
    })
