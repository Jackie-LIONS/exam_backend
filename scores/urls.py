from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_exam, name='submit_exam'),
    path('add/', views.add_score, name='add_score'),
    path('', views.get_all_scores, name='get_all_scores'),
    path('user/<int:user_id>/', views.get_user_scores, name='get_user_scores'),
    path('exam/<int:exam_id>/', views.get_exam_scores, name='get_exam_scores'),
    path('history/<int:user_id>/', views.get_exam_history, name='get_exam_history'),
]