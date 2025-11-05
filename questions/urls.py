from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_questions, name='get_questions'),
    path('get/<int:question_id>/', views.get_question, name='get_question'),
    path('add/', views.add_question, name='add_question'),
    path('update/<int:question_id>/', views.update_question, name='update_question'),
    path('delete/<int:question_id>/', views.delete_question, name='delete_question'),
]