# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Test, Question, Choice, TestResult, ElementType
from .forms import TestForm

def test_list(request):
    tests = Test.objects.all()
    return render(request, 'test_list.html', {'tests': tests})

@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    
    if request.method == 'POST':
        form = TestForm(test, request.POST)
        if form.is_valid():
            # Element puanlarını hesapla
            fire_score = 0
            air_score = 0
            water_score = 0
            earth_score = 0
            
            for field_name, choice_id in form.cleaned_data.items():
                choice = get_object_or_404(Choice, id=choice_id)
                element = choice.element_type.name
                
                if element == 'Ateş':
                    fire_score += choice.score
                elif element == 'Hava':
                    air_score += choice.score
                elif element == 'Su':
                    water_score += choice.score
                elif element == 'Toprak':
                    earth_score += choice.score
            
            # Sonucu kaydet
            result = TestResult(
                user=request.user,
                test=test,
                fire_score=fire_score,
                air_score=air_score,
                water_score=water_score,
                earth_score=earth_score
            )
            
            # En yüksek element puanını bul
            result.calculate_dominant_element()
            
            return redirect('test_result', result_id=result.id)
    else:
        form = TestForm(test)
    
    return render(request, 'take_test.html', {'form': form, 'test': test})

@login_required
def test_result(request, result_id):
    result = get_object_or_404(TestResult, id=result_id, user=request.user)
    
    # Toplam puan hesapla
    total_score = result.fire_score + result.air_score + result.water_score + result.earth_score
    
    # Yüzde hesapla
    element_scores = {
        'Ateş': int((result.fire_score / total_score) * 100) if total_score > 0 else 0,
        'Hava': int((result.air_score / total_score) * 100) if total_score > 0 else 0,
        'Su': int((result.water_score / total_score) * 100) if total_score > 0 else 0,
        'Toprak': int((result.earth_score / total_score) * 100) if total_score > 0 else 0
    }
    
    context = {
        'result': result,
        'element_scores': element_scores,
        'dominant_element': result.dominant_element,
    }
    
    return render(request, 'test_result.html', context)

def element_detail(request, element_id):
    element = get_object_or_404(ElementType, id=element_id)
    return render(request, 'element_detail.html', {'element': element})
