# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Test, Choice, Question, TestResult, ElementType, TestResultDetail

def direct_to_test(request):
    first_test = Test.objects.first()
    if first_test:
        # Kullanıcı giriş yapmışsa
        if request.user.is_authenticated:
            # Kullanıcının daha önce testi çözüp çözmediğini kontrol et
            existing_result = TestResult.objects.filter(user=request.user, test=first_test).first()
            if existing_result:
                # Daha önce test çözülmüşse sonuç sayfasına yönlendir
                return redirect('test_result', result_id=existing_result.id)
        
        # Eğer kullanıcı giriş yapmamışsa veya daha önce test çözmediyse teste yönlendir
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

    # Kullanıcı daha önce bu testi tamamlamış mı kontrol et
    # Bu kontrol artık oturum bilgisine bakacak, veritabanına değil
    if 'test_phase' not in request.session:
        request.session['test_phase'] = 'WARM'
        request.session['warm_score'] = 0
        request.session['cold_score'] = 0
        request.session['moist_score'] = 0
        request.session['dry_score'] = 0
        request.session['test_answers'] = {}
        request.session.modified = True

    # İlk aşama soruları (Sıcak/Soğuk)
    warm_questions = list(test.questions.filter(question_type='WARM').order_by('order'))
    warm_questions_count = len(warm_questions)
    
    # İkinci aşama soruları (Mizaç tipine göre ayrı Kuru/Nemli soruları)
    warm_moist_questions = list(test.questions.filter(question_type='WARM_MOIST').order_by('order'))
    cold_moist_questions = list(test.questions.filter(question_type='COLD_MOIST').order_by('order'))
    
    
    # Test oturumunu başlat
    if 'test_phase' not in request.session:
        request.session['test_phase'] = 'WARM'
        # Sıcak/soğuk puanları
        request.session['warm_score'] = 0
        request.session['cold_score'] = 0
        # Nemli/kuru puanları
        request.session['moist_score'] = 0
        request.session['dry_score'] = 0
        # Cevapları sakla
        request.session['test_answers'] = {}
        request.session.modified = True
    
    # İlk aşamadan sonra ikinci aşama tipini belirle
    if question_index == warm_questions_count and request.session['test_phase'] == 'WARM':
        warm_score = request.session.get('warm_score', 0)
        cold_score = request.session.get('cold_score', 0)
        
        # Net sıcaklık puanını hesapla (sıcak - soğuk)
        net_warm_score = warm_score - cold_score
        
        if net_warm_score >= 0:  # Sıcak
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
    
    # Mevcut soru ve seçenekleri belirle
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
                # Tüm sorular tamamlandı
                # Ham puanları al
                warm_score = request.session.get('warm_score', 0)
                cold_score = request.session.get('cold_score', 0)
                moist_score = request.session.get('moist_score', 0)
                dry_score = request.session.get('dry_score', 0)
                answers = request.session.get('test_answers', {})
                
                # Net puanları hesapla
                net_warm_score = warm_score - cold_score
                net_moist_score = moist_score - dry_score
                
                # Dominant elementi belirle
                is_warm = net_warm_score >= 0
                is_moist = net_moist_score >= 0
                
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
                    warm_score=net_warm_score,
                    moist_score=net_moist_score,
                    # Ham puanları da kaydet
                    raw_warm_score=warm_score,
                    raw_cold_score=cold_score,
                    raw_moist_score=moist_score,
                    raw_dry_score=dry_score,
                    dominant_element=dominant_element
                )
                result.save()
                
                # Detay kayıtları oluştur
                for question_id, choice_id in answers.items():
                    choice = get_object_or_404(Choice, id=choice_id)
                    question_id_cleaned = int(question_id.replace('question_', ''))
                    question = get_object_or_404(Question, id=question_id_cleaned)
                    
                    # Doğru skor tipini belirle
                    if question.question_type == 'WARM':
                        score = choice.warm_score - choice.cold_score  # Net sıcaklık puanı
                        TestResultDetail.objects.create(
                            test_result=result,
                            question=question,
                            selected_choice=choice,
                            score=score,
                            warm_score=choice.warm_score,
                            cold_score=choice.cold_score,
                            moist_score=0,
                            dry_score=0
                        )
                    else:  # WARM_MOIST veya COLD_MOIST
                        score = choice.moist_score - choice.dry_score  # Net nem puanı
                        TestResultDetail.objects.create(
                            test_result=result,
                            question=question,
                            selected_choice=choice,
                            score=score,
                            warm_score=0,
                            cold_score=0,
                            moist_score=choice.moist_score,
                            dry_score=choice.dry_score
                        )
                
                # Oturum verilerini temizle
                for key in ['test_phase', 'warm_score', 'cold_score', 'moist_score', 'dry_score', 'test_answers']:
                    if key in request.session:
                        del request.session[key]
                
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
                request.session['warm_score'] += selected_choice.warm_score
                request.session['cold_score'] += selected_choice.cold_score
            else:  # WARM_MOIST veya COLD_MOIST
                request.session['moist_score'] += selected_choice.moist_score
                request.session['dry_score'] += selected_choice.dry_score
            
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
    
    # Net skorlar
    net_warm_score = result.warm_score  # Zaten net değer saklanıyor
    net_moist_score = result.moist_score  # Zaten net değer saklanıyor
    
    # Ham skorlar
    raw_warm_score = result.raw_warm_score
    raw_cold_score = result.raw_cold_score
    raw_moist_score = result.raw_moist_score
    raw_dry_score = result.raw_dry_score
    
    # Sıcaklık ve nem özelliklerini metin olarak belirle
    warmth_text = "Sıcak" if net_warm_score >= 0 else "Soğuk"
    moisture_text = "Nemli" if net_moist_score >= 0 else "Kuru"
    
    # Skorların mutlak değerlerini şiddet göstergesi olarak kullan (0-10 arasında normalize et)
    max_intensity = 10  # Maksimum yoğunluk değeri
    
    # Sıcaklık yoğunluğu (pozitif değer olarak)
    warmth_intensity = min(abs(net_warm_score), max_intensity)
    
    # Nem yoğunluğu (pozitif değer olarak)
    moisture_intensity = min(abs(net_moist_score), max_intensity)
    
    # Ölçek boyutunu 10 üzerinden hesapla
    scale_percentage_warmth = int((warmth_intensity / max_intensity) * 100)
    scale_percentage_moisture = int((moisture_intensity / max_intensity) * 100)
    
    context = {
        'result': result,
        'dominant_element': result.dominant_element,
        'warmth_text': warmth_text,
        'moisture_text': moisture_text,
        'warmth_intensity': warmth_intensity,
        'moisture_intensity': moisture_intensity,
        'scale_percentage_warmth': scale_percentage_warmth,
        'scale_percentage_moisture': scale_percentage_moisture,
        # Ham skorları da gönder
        'raw_warm_score': raw_warm_score,
        'raw_cold_score': raw_cold_score,
        'raw_moist_score': raw_moist_score,
        'raw_dry_score': raw_dry_score,
    }
    
    return render(request, 'testing_algorithm/test_result.html', context)

def element_detail(request, element_id):
    element = get_object_or_404(ElementType, id=element_id)
    return render(request, 'testing_algorithm/element_detail.html', {'element': element})