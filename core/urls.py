from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('quiz/<slug:slug>/', views.quiz_view, name='quiz'),
    path('assessment/<slug:slug>/', views.assessment_view, name='assessment'),
]
