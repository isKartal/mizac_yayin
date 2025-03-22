# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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
    question_count = test.questions.count()
    
    return render(request, 'testing_algorithm/test_intro.html', {
        'test': test,
        'question_count': question_count
    })

@login_required
def take_test(request, test_id, question_index=0):
    test = get_object_or_404(Test, id=test_id)

    existing_result = TestResult.objects.filter(user=request.user, test=test).first()
    if existing_result:
        return redirect('test_result', result_id=existing_result.id)

    questions = list(test.questions.all())
    total_questions = len(questions)

    if question_index >= total_questions:
        answers = request.session.get('test_answers', {})

        fire_score = 0
        air_score = 0
        water_score = 0
        earth_score = 0
        
        # Calculate scores first
        for question_id, choice_id in answers.items():
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
        
        # Find the dominant element
        scores = {
            'Ateş': fire_score,
            'Hava': air_score,
            'Su': water_score,
            'Toprak': earth_score
        }
        dominant_name = max(scores, key=scores.get)
        dominant_element = ElementType.objects.filter(name=dominant_name).first()
        
        # Now create the TestResult with the correct dominant element
        result = TestResult(
            user=request.user,
            test=test,
            fire_score=fire_score,
            air_score=air_score,
            water_score=water_score,
            earth_score=earth_score,
            dominant_element=dominant_element  # Set the dominant element here
        )
        result.save()
        
        request.session['test_result_id'] = result.id
        
        # Create detail records
        for question_id, choice_id in answers.items():
            choice = get_object_or_404(Choice, id=choice_id)
            question_id_cleaned = int(question_id.replace('question_', ''))
            question = get_object_or_404(Question, id=question_id_cleaned)
            
            TestResultDetail.objects.create(
                test_result=result,
                question=question,
                selected_choice=choice,
                score=choice.score,
                element_type=choice.element_type
            )
        
        return redirect('test_result', result_id=result.id)

    # Rest of the code remains the same...
    
    current_question = questions[question_index]
    choices = Choice.objects.filter(question=current_question)

    if request.method == 'POST':
        selected_choice_id = request.POST.get('choice')
        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)

            if 'test_answers' not in request.session:
                request.session['test_answers'] = {}

            request.session['test_answers'][f'question_{current_question.id}'] = selected_choice.id
            request.session.modified = True

            return redirect('take_test', test_id=test_id, question_index=question_index + 1)

    return render(request, 'testing_algorithm/take_test.html', {
        'test': test,
        'current_question': current_question,
        'choices': choices,
        'question_index': question_index,
        'total_questions': total_questions
    })

@login_required
def test_result(request, result_id):
    result = get_object_or_404(TestResult, id=result_id, user=request.user)
    
    total_score = result.fire_score + result.air_score + result.water_score + result.earth_score
    
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
    
    return render(request, 'testing_algorithm/test_result.html', context)
