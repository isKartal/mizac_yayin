from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('start-test/', views.start_test, name='start_test'),
    path('more/', views.more, name='more'),
    path('temperaments/', views.temperaments, name='temperaments'),
]