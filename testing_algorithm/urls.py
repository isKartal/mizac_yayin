# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('tests/', views.direct_to_test, name='test_list'),
    path('tests/<int:test_id>/<int:question_index>/', views.take_test, name='take_test'),
    path('results/<int:result_id>/', views.test_result, name='test_result'),
    path('elements/<int:element_id>/', views.element_detail, name='element_detail'),
]