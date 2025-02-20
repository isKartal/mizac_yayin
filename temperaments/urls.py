from django.urls import path
from . import views

urlpatterns = [
    path('temperaments', views.temperaments, name='temperaments'),
    path('fire_more/', views.fire_more, name='fire_more'),
    path('water_more/', views.water_more, name='water_more'),
    path('earth_more/', views.earth_more, name='earth_more'),
    path('air_more/', views.air_more, name='air_more'),
]