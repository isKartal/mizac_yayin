# urls.py
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('tests/', views.direct_to_test, name='test_list'),
    path('tests/<int:test_id>/<int:question_index>/', views.take_test, name='take_test'),
    path('results/<int:result_id>/', views.test_result, name='test_result'),
    path('tests/<int:test_id>/intro/', views.test_intro, name='test_intro'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)