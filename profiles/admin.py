# profiles/admin.py
from django.contrib import admin
from .models import ContentCategory, RecommendedContent, UserContentInteraction

@admin.register(ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(RecommendedContent)
class RecommendedContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'related_element_name', 'is_active', 'created_at', 'order')
    list_filter = ('is_active', 'category', 'related_element_name')
    search_fields = ('title', 'short_description', 'content')
    list_editable = ('is_active', 'order')
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'short_description', 'content', 'image')
        }),
        ('Kategorizasyon', {
            'fields': ('category', 'related_element_name')
        }),
        ('Ayarlar', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(UserContentInteraction)
class UserContentInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'viewed', 'liked', 'saved', 'viewed_at')
    list_filter = ('viewed', 'liked', 'saved')
    search_fields = ('user__username', 'content__title')
    date_hierarchy = 'viewed_at'
    readonly_fields = ('viewed_at',)