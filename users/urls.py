from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('me/', views.get_current_user, name='get_current_user'),
    path('', views.get_users, name='get_users'),
    path('get/<int:user_id>/', views.get_user, name='get_user'),
    path('update/<int:user_id>/', views.update_user, name='update_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('dashboard/stats/', views.get_dashboard_stats, name='get_dashboard_stats'),
    path('student/stats/', views.get_student_stats, name='get_student_stats'),
]