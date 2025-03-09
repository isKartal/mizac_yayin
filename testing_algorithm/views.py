# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Test, Choice, TestResult, ElementType

def direct_to_test(request):
    first_test = Test.objects.first()
    if first_test:
        return redirect('take_test', test_id=first_test.id, question_index=0)
    return redirect('/')

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

        result = TestResult(
            user=request.user,
            test=test,
            fire_score=fire_score,
            air_score=air_score,
            water_score=water_score,
            earth_score=earth_score
        )

        result.calculate_dominant_element()
        request.session['test_result_id'] = result.id

        return redirect('test_result', result_id=result.id)

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

def element_detail(request, element_id):
    element = get_object_or_404(ElementType, id=element_id)
    return render(request, 'testing_algorithm/element_detail.html', {'element': element})
