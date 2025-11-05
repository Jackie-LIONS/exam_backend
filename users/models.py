from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('student', '学生'),
    )
    
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'User'
