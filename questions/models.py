from django.db import models
import json

class Question(models.Model):
    TYPE_CHOICES = (
        ('choice', '选择题'),
        ('true_false', '判断题'),
        ('fill_in_blank', '填空题'),
        ('essay', '简答题'),
    )
    
    DIFFICULTY_CHOICES = (
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难'),
    )
    
    CHOICE_TYPE_CHOICES = (
        ('single', '单选题'),
        ('multiple', '多选题'),
    )
    
    question_id = models.AutoField(primary_key=True)
    content = models.TextField()
    question_type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    
    # 选择题相关字段
    choice_type = models.CharField(max_length=10, choices=CHOICE_TYPE_CHOICES, null=True, blank=True)
    options = models.JSONField(null=True, blank=True, help_text='选择题选项，JSON格式存储')
    
    # 判断题答案
    true_false_answer = models.BooleanField(null=True, blank=True, help_text='判断题答案')
    
    # 填空题答案
    fill_answer = models.TextField(null=True, blank=True, help_text='填空题标准答案')
    
    # 简答题答案
    essay_answer = models.TextField(null=True, blank=True, help_text='简答题参考答案')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Question'
    
    def __str__(self):
        return f"{self.get_question_type_display()}: {self.content[:50]}..."
