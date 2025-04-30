from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.profiles, name='profiles'),
    path('my_suggestions/', views.my_suggestions, name='my_suggestions'),
    path('my_temperament/', views.my_temperament, name='my_temperament'),
    path('restart_test/', views.restart_test, name='restart_test'),
    path('content/<int:content_id>/detail/', views.content_detail, name='content_detail'),
    path('content/<int:content_id>/toggle_like/', views.toggle_like_content, name='toggle_like_content'),
    path('content/<int:content_id>/toggle_save/', views.toggle_save_content, name='toggle_save_content'),
    path('api/all_contents/', views.api_all_contents, name='api_all_contents'),
]