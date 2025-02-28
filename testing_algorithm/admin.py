# admin.py
from django.contrib import admin
from .models import ElementType, Test, Question, Choice, TestResult

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3

class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(ElementType)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TestResult)