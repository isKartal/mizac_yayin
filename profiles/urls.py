from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.profiles, name='profiles'),
    path('my_suggestions/', views.my_suggestions, name='my_suggestions'),
    path('my_temperament/', views.my_temperament, name='my_temperament'),
    path('restart_test/', views.restart_test, name='restart_test'),
]
