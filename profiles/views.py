from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from testing_algorithm.models import TestResult, ElementType 

@login_required
def profiles(request):
    """ Profil ana sayfasını gösterir """
    return render(request, 'profiles/profiles.html')

@login_required
def my_temperament(request):
    test_result = TestResult.objects.filter(user=request.user).order_by('-date_taken').first()
    if test_result:
        dominant = test_result.dominant_element.name
        if dominant == "Ateş":
            return redirect('fire_more')
        elif dominant == "Hava":
            return redirect('air_more')
        elif dominant == "Su":
            return redirect('water_more')
        elif dominant == "Toprak":
            return redirect('earth_more')
    # Eğer test sonucu yoksa, kullanıcıyı teste yönlendirebilirsiniz
    return redirect('test_list')

@login_required
def my_suggestions(request):
    return render(request, 'profiles/not_active.html')

