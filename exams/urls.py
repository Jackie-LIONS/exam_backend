from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_exams, name='get_exams'),
    path('get/<int:exam_id>/', views.get_exam, name='get_exam'),
    path('create/', views.create_exam, name='create_exam'),
    path('update/<int:exam_id>/', views.update_exam, name='update_exam'),
    path('delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('add_question/', views.add_question_to_exam, name='add_question_to_exam'),
    path('questions/<int:exam_id>/', views.get_exam_questions, name='get_exam_questions'),
    path('remove_question/<int:exam_question_id>/', views.remove_question_from_exam, name='remove_question_from_exam'),
    path('generate_paper/', views.generate_exam_paper, name='generate_exam_paper'),
]