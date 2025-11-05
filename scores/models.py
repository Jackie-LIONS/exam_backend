from django.db import models
from users.models import User
from exams.models import Exam

class Score(models.Model):
    score_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Score'

class ExamHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ExamHistory'
