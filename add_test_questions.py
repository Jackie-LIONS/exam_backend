#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_backend.settings')
django.setup()

from questions.models import Question

# 添加判断题
judge_questions = [
    {'content': '地球是圆的', 'difficulty': 'easy', 'answer': '正确'},
    {'content': '太阳从西边升起', 'difficulty': 'easy', 'answer': '错误'},
    {'content': '水的沸点是100摄氏度', 'difficulty': 'easy', 'answer': '正确'},
    {'content': '光速是宇宙中最快的速度', 'difficulty': 'medium', 'answer': '正确'},
    {'content': '量子力学中的不确定性原理是正确的', 'difficulty': 'medium', 'answer': '正确'},
    {'content': '相对论改变了我们对时空的理解', 'difficulty': 'hard', 'answer': '正确'},
    {'content': '黑洞的事件视界是不可逆的边界', 'difficulty': 'hard', 'answer': '正确'},
]

print("添加判断题...")
for q in judge_questions:
    Question.objects.create(
        content=q['content'],
        question_type='judge',
        difficulty_level=q['difficulty'],
        answer=q['answer']
    )
    print(f"添加判断题: {q['content'][:20]}...")

# 添加填空题
fill_questions = [
    {'content': '地球的半径约为____公里', 'difficulty': 'easy', 'answer': '6371'},
    {'content': '一年有____个月', 'difficulty': 'easy', 'answer': '12'},
    {'content': '圆周率π的值约为____', 'difficulty': 'easy', 'answer': '3.14'},
    {'content': '牛顿第二定律的公式是____', 'difficulty': 'medium', 'answer': 'F=ma'},
    {'content': '化学元素周期表中氢的原子序数是____', 'difficulty': 'medium', 'answer': '1'},
    {'content': '爱因斯坦质能方程是____', 'difficulty': 'hard', 'answer': 'E=mc²'},
    {'content': '薛定谔方程描述了____的演化', 'difficulty': 'hard', 'answer': '量子系统'},
]

print("添加填空题...")
for q in fill_questions:
    Question.objects.create(
        content=q['content'],
        question_type='fill',
        difficulty_level=q['difficulty'],
        answer=q['answer']
    )
    print(f"添加填空题: {q['content'][:20]}...")

print("所有题目添加完成！")

# 统计题目数量
print("\n题目数量统计：")
question_types = ['choice', 'judge', 'fill', 'essay']
difficulties = ['easy', 'medium', 'hard']

for qtype in question_types:
    print(f"\n{qtype}类型题目：")
    for difficulty in difficulties:
        count = Question.objects.filter(question_type=qtype, difficulty_level=difficulty).count()
        print(f"  {difficulty}: {count}道")