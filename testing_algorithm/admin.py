# admin.py
import nested_admin
from django.contrib import admin
from .models import ElementType, Test, Question, Choice, TestResult, TestResultDetail

class ElementTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_warm', 'is_moist')

admin.site.register(ElementType, ElementTypeAdmin)

# Test için nested inline yapılandırması
class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 2  # İki seçenek (Evet/Hayır için)

class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]
    list_display = ('text', 'question_type', 'order')
    list_filter = ('question_type',)

class TestAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'description')
    inlines = [QuestionInline]

admin.site.register(Test, TestAdmin)

class QuestionAdmin(nested_admin.NestedModelAdmin):
    list_display = ('text', 'test', 'question_type', 'order')
    list_filter = ('question_type', 'test')
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    # 'score' yerine yeni puan alanlarını göster
    list_display = ('text', 'question', 'warm_score', 'cold_score', 'moist_score', 'dry_score')
    list_filter = ('question__question_type',)

admin.site.register(Choice, ChoiceAdmin)

# TestResultDetail için admin yapılandırması
class TestResultDetailInline(admin.TabularInline):
    model = TestResultDetail
    readonly_fields = ('question', 'selected_choice', 'score')
    extra = 0
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

# TestResult için admin yapılandırması
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'dominant_element', 'warm_score', 'moist_score', 'date_taken')
    list_filter = ('user', 'test', 'dominant_element')
    readonly_fields = ('date_taken', 'warm_score', 'moist_score', 'dominant_element')
    inlines = [TestResultDetailInline]
    
    fieldsets = (
        ('Kullanıcı Bilgileri', {
            'fields': ('user', 'test', 'date_taken')
        }),
        ('Skorlar', {
            'fields': ('warm_score', 'moist_score', 'dominant_element')
        }),
    )

admin.site.register(TestResult, TestResultAdmin)