from django.db import models
from questions.models import Question

class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField()  # 考试时长（分钟）
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Exam'

class ExamQuestion(models.Model):
    exam_question_id = models.AutoField(primary_key=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'ExamQuestion'
