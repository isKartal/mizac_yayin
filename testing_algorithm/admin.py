# admin.py
import nested_admin
from django.contrib import admin
from .models import ElementType, Test, Question, Choice, TestResult, TestResultDetail

class ElementTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(ElementType, ElementTypeAdmin)

# Test için nested inline yapılandırması
class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 1

class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]

class TestAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'description')
    inlines = [QuestionInline]

admin.site.register(Test, TestAdmin)

class QuestionAdmin(nested_admin.NestedModelAdmin):
    list_display = ('text', 'test')
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'element_type', 'score')

admin.site.register(Choice, ChoiceAdmin)

# TestResultDetail için admin yapılandırması
class TestResultDetailInline(admin.TabularInline):
    model = TestResultDetail
    readonly_fields = ('question', 'selected_choice', 'score', 'element_type')
    extra = 0
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

# TestResult için admin yapılandırması
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'dominant_element', 'fire_score', 'air_score', 'water_score', 'earth_score', 'date_taken')
    list_filter = ('user', 'test', 'dominant_element')
    readonly_fields = ('date_taken', 'fire_score', 'air_score', 'water_score', 'earth_score', 'dominant_element')
    inlines = [TestResultDetailInline]
    
    fieldsets = (
        ('Kullanıcı Bilgileri', {
            'fields': ('user', 'test', 'date_taken')
        }),
        ('Element Puanları', {
            'fields': ('fire_score', 'air_score', 'water_score', 'earth_score', 'dominant_element')
        }),
    )

admin.site.register(TestResult, TestResultAdmin)