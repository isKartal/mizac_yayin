# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Test, Choice, Question, TestResult, ElementType, TestResultDetail

def direct_to_test(request):
    first_test = Test.objects.first()
    if first_test:
        return redirect('test_intro', test_id=first_test.id)
    return redirect('/')

@login_required
def test_intro(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    
    # Kullanıcı daha önce bu testi tamamlamış mı kontrol et
    existing_result = TestResult.objects.filter(user=request.user, test=test).first()
    if existing_result:
        return redirect('test_result', result_id=existing_result.id)
    
    # Test hakkında bilgileri hazırla
    warm_questions_count = test.questions.filter(question_type='WARM').count()
    
    # Sıcak ve soğuk için ayrı ayrı kuru/nemli soru sayıları
    warm_moist_questions_count = test.questions.filter(question_type='WARM_MOIST').count()
    cold_moist_questions_count = test.questions.filter(question_type='COLD_MOIST').count()
    
    # Tahmini toplam soru sayısı (varsayılan olarak sıcak yolu kullanılır)
    total_questions = warm_questions_count + max(warm_moist_questions_count, cold_moist_questions_count)
    
    return render(request, 'testing_algorithm/test_intro.html', {
        'test': test,
        'question_count': total_questions,
        'warm_questions_count': warm_questions_count,
        'moist_questions_count': max(warm_moist_questions_count, cold_moist_questions_count)
    })

@login_required
def take_test(request, test_id, question_index=0):
    test = get_object_or_404(Test, id=test_id)

    # Kullanıcı daha önce testi tamamlamış mı kontrol et
    existing_result = TestResult.objects.filter(user=request.user, test=test).first()
    if existing_result:
        return redirect('test_result', result_id=existing_result.id)

    # İlk aşama soruları (Sıcak/Soğuk)
    warm_questions = list(test.questions.filter(question_type='WARM').order_by('order'))
    warm_questions_count = len(warm_questions)
    
    # İkinci aşama soruları (Mizaç tipine göre ayrı Kuru/Nemli soruları)
    warm_moist_questions = list(test.questions.filter(question_type='WARM_MOIST').order_by('order'))
    cold_moist_questions = list(test.questions.filter(question_type='COLD_MOIST').order_by('order'))
    
    # Test oturumunu başlat
    if 'test_phase' not in request.session:
        request.session['test_phase'] = 'WARM'
        request.session['warm_score'] = 0
        request.session['moist_score'] = 0
        request.session['test_answers'] = {}
        request.session.modified = True
    
    # İlk aşamadan sonra ikinci aşama tipini belirle
    if question_index == warm_questions_count and request.session['test_phase'] == 'WARM':
        warm_score = request.session.get('warm_score', 0)
        if warm_score >= 0:  # Sıcak
            request.session['test_phase'] = 'WARM_MOIST'
        else:  # Soğuk
            request.session['test_phase'] = 'COLD_MOIST'
        request.session.modified = True
    
    # Dinamik olarak toplam soru sayısını hesapla
    current_phase = request.session.get('test_phase')
    if current_phase == 'WARM_MOIST':
        total_questions = warm_questions_count + len(warm_moist_questions)
        moist_questions = warm_moist_questions
    elif current_phase == 'COLD_MOIST':
        total_questions = warm_questions_count + len(cold_moist_questions)
        moist_questions = cold_moist_questions
    else:
        # Henüz sıcak/soğuk belirlenmemişse, varsayılan olarak sıcak yolunu kullan
        total_questions = warm_questions_count + len(warm_moist_questions)
        moist_questions = []
    
    # Tüm sorular tamamlandı mı kontrol et ve sonucu hesapla
    if question_index >= total_questions:
        warm_score = request.session.get('warm_score', 0)
        moist_score = request.session.get('moist_score', 0)
        answers = request.session.get('test_answers', {})
        
        # Dominant elementi belirle
        is_warm = warm_score >= 0
        is_moist = moist_score >= 0
        
        # Mizaç türünü belirle
        if is_warm and not is_moist:  # Sıcak ve Kuru = Ateş
            element_name = "Ateş"
        elif is_warm and is_moist:    # Sıcak ve Nemli = Hava
            element_name = "Hava"
        elif not is_warm and is_moist:  # Soğuk ve Nemli = Su
            element_name = "Su"
        else:  # Soğuk ve Kuru = Toprak
            element_name = "Toprak"
        
        dominant_element = ElementType.objects.filter(name=element_name).first()
        
        # TestResult oluştur
        result = TestResult(
            user=request.user,
            test=test,
            warm_score=warm_score,
            moist_score=moist_score,
            dominant_element=dominant_element
        )
        result.save()
        
        # Detay kayıtları oluştur
        for question_id, choice_id in answers.items():
            choice = get_object_or_404(Choice, id=choice_id)
            question_id_cleaned = int(question_id.replace('question_', ''))
            question = get_object_or_404(Question, id=question_id_cleaned)
            
            TestResultDetail.objects.create(
                test_result=result,
                question=question,
                selected_choice=choice,
                score=choice.score
            )
        
        # Oturum verilerini temizle
        for key in ['test_phase', 'warm_score', 'moist_score', 'test_answers']:
            if key in request.session:
                del request.session[key]
        
        return redirect('test_result', result_id=result.id)
    
    # Mevcut soru ve seçenekleri belirle
    current_phase = request.session.get('test_phase')
    
    if current_phase == 'WARM':
        if question_index < warm_questions_count:
            current_question = warm_questions[question_index]
        else:
            # Bu durum normalde gerçekleşmemeli, ama güvenlik için kontrol
            return redirect('take_test', test_id=test_id, question_index=warm_questions_count)
    else:  # WARM_MOIST veya COLD_MOIST
        if question_index < warm_questions_count:
            # Bu durum normalde gerçekleşmemeli, ama güvenlik için kontrol
            return redirect('take_test', test_id=test_id, question_index=warm_questions_count)
        else:
            adjusted_index = question_index - warm_questions_count
            if adjusted_index < len(moist_questions):
                current_question = moist_questions[adjusted_index]
            else:
                # Bu durum normalde gerçekleşmemeli, ama güvenlik için kontrol
                return redirect('test_result', result_id=result.id)
    
    choices = Choice.objects.filter(question=current_question)
    
    # POST işlemini ele al (kullanıcı bir cevap gönderdiğinde)
    if request.method == 'POST':
        selected_choice_id = request.POST.get('choice')
        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)
            
            # Cevabı kaydet
            request.session['test_answers'][f'question_{current_question.id}'] = selected_choice.id
            
            # Skoru güncelle
            if current_phase == 'WARM':
                request.session['warm_score'] += selected_choice.score
            else:  # WARM_MOIST veya COLD_MOIST
                request.session['moist_score'] += selected_choice.score
            
            request.session.modified = True
            
            return redirect('take_test', test_id=test_id, question_index=question_index + 1)
    
    # İlerleme durumunu hesapla
    progress_percentage = int((question_index / total_questions) * 100) if total_questions > 0 else 0
    
    # Faz adını kullanıcı dostu yap
    phase_display = {
        'WARM': 'Sıcak/Soğuk Özellikleri',
        'WARM_MOIST': 'Sıcak Mizaçlar için Kuru/Nemli Özellikleri',
        'COLD_MOIST': 'Soğuk Mizaçlar için Kuru/Nemli Özellikleri'
    }.get(current_phase, 'Test Soruları')
    
    return render(request, 'testing_algorithm/take_test.html', {
        'test': test,
        'current_question': current_question,
        'choices': choices,
        'question_index': question_index,
        'total_questions': total_questions,
        'progress_percentage': progress_percentage,
        'phase': phase_display
    })

@login_required
def test_result(request, result_id):
    result = get_object_or_404(TestResult, id=result_id, user=request.user)
    
    # Sonuçlar için metin oluştur
    is_warm = result.warm_score >= 0
    is_moist = result.moist_score >= 0
    
    # Sıcaklık ve nem özelliklerini metin olarak belirle
    warmth_text = "Sıcak" if is_warm else "Soğuk"
    moisture_text = "Nemli" if is_moist else "Kuru"
    
    # Skorların mutlak değerlerini şiddet göstergesi olarak kullan
    warmth_intensity = min(abs(result.warm_score), 10)  # Maksimum 10 ile sınırla
    moisture_intensity = min(abs(result.moist_score), 10)  # Maksimum 10 ile sınırla
    
    context = {
        'result': result,
        'dominant_element': result.dominant_element,
        'warmth_text': warmth_text,
        'moisture_text': moisture_text,
        'warmth_intensity': warmth_intensity,
        'moisture_intensity': moisture_intensity,
    }
    
    return render(request, 'testing_algorithm/test_result.html', context)

def element_detail(request, element_id):
    element = get_object_or_404(ElementType, id=element_id)
    return render(request, 'testing_algorithm/element_detail.html', {'element': element})