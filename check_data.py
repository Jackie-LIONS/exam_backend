#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')
django.setup()

from users.models import User
from questions.models import Question  
from exams.models import Exam
from scores.models import Score
from django.utils import timezone
from django.db.models import Avg

print('=== 数据库统计 ===')
print(f'学生总数: {User.objects.filter(role="student").count()}')
print(f'题目总数: {Question.objects.count()}')

now = timezone.now()
ongoing = Exam.objects.filter(start_time__lte=now, end_time__gte=now).count()
print(f'进行中考试: {ongoing}')

avg_score = Score.objects.aggregate(avg_score=Avg('score'))['avg_score']
print(f'平均分数: {avg_score or 0}')

print(f'总考试数: {Exam.objects.count()}')
print(f'总成绩记录: {Score.objects.count()}')

# 检查是否有测试数据
print('\n=== 详细信息 ===')
users = User.objects.all()[:5]
for user in users:
    print(f'用户: {user.username} - 角色: {user.role}')

exams = Exam.objects.all()[:3]
for exam in exams:
    print(f'考试: {exam.exam_name} - 开始时间: {exam.start_time} - 结束时间: {exam.end_time}')