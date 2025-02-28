# forms.py
from django import forms
from .models import Test, Question, Choice

class TestForm(forms.Form):
    def __init__(self, test, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        questions = Question.objects.filter(test=test)
        
        for i, question in enumerate(questions):
            choices = Choice.objects.filter(question=question)
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=[(choice.id, choice.text) for choice in choices],
                widget=forms.RadioSelect
            )