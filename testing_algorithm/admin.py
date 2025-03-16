# admin.py
import nested_admin
from django.contrib import admin
from .models import ElementType, Recommendation, Test, Question, Choice, TestResult

# ElementType için Recommendation inline'ı (nested inline kullanılabilir)
class RecommendationInline(nested_admin.NestedTabularInline):
    model = Recommendation
    extra = 1  # Varsayılan olarak 1 boş form

class ElementTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [RecommendationInline]

admin.site.register(ElementType, ElementTypeAdmin)

# Test için nested inline yapılandırması: Test > Question > Choice

class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 1  # Her soru için varsayılan 1 boş şık formu

class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    extra = 1  # Her test için varsayılan 1 boş soru formu
    inlines = [ChoiceInline]  # Her soruya ait şıkları inline ekle

class TestAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'description')
    inlines = [QuestionInline]

admin.site.register(Test, TestAdmin)

# Eğer ayrı olarak da düzenlemek isterseniz, Question ve Choice için standart adminler:
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test')
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'element_type', 'score')

admin.site.register(Choice, ChoiceAdmin)

# TestResult için basit bir admin yapılandırması:
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'dominant_element', 'date_taken')
    list_filter = ('user', 'test', 'dominant_element')

admin.site.register(TestResult, TestResultAdmin)
