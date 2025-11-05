#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')
django.setup()

from users.models import User
from exams.models import Exam
from scores.models import Score
from django.utils import timezone

# 获取学生用户
students = User.objects.filter(role='student')
exams = Exam.objects.all()

print('=== 添加测试数据 ===')

# 1. 修改考试时间，让部分考试处于进行中状态
now = timezone.now()

if exams.exists():
    # 第一个考试设为进行中（开始时间是1小时前，结束时间是1小时后）
    exam1 = exams[0]
    exam1.start_time = now - timedelta(hours=1)
    exam1.end_time = now + timedelta(hours=1)
    exam1.save()
    print(f'修改考试 "{exam1.exam_name}" 为进行中状态')
    
    if len(exams) > 1:
        # 第二个考试也设为进行中
        exam2 = exams[1]
        exam2.start_time = now - timedelta(minutes=30)
        exam2.end_time = now + timedelta(hours=2)
        exam2.save()
        print(f'修改考试 "{exam2.exam_name}" 为进行中状态')

# 2. 为学生添加一些成绩记录
scores_data = [
    {'score': 85.5},
    {'score': 92.0},
    {'score': 78.5},
    {'score': 88.0},
    {'score': 95.5},
    {'score': 76.0},
    {'score': 89.5},
    {'score': 82.0}
]

# 清除现有成绩记录
Score.objects.all().delete()

# 添加新的成绩记录
for i, score_data in enumerate(scores_data):
    if students.exists() and exams.exists():
        student = students[i % len(students)]
        exam = exams[i % len(exams)]
        
        score = Score.objects.create(
            user=student,
            exam=exam,
            score=score_data['score']
        )
        print(f'为学生 {student.username} 在考试 "{exam.exam_name}" 中添加成绩: {score_data["score"]}')

print('\n=== 数据添加完成 ===')

# 验证数据
from django.db.models import Avg
ongoing = Exam.objects.filter(start_time__lte=now, end_time__gte=now).count()
avg_score = Score.objects.aggregate(avg_score=Avg('score'))['avg_score']

print(f'进行中考试数量: {ongoing}')
print(f'平均分数: {round(avg_score, 1) if avg_score else 0}')
print(f'成绩记录总数: {Score.objects.count()}')