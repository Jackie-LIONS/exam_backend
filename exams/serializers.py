from rest_framework import serializers
from .models import Exam, ExamQuestion
from questions.serializers import QuestionSerializer

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['exam_id', 'exam_name', 'start_time', 'end_time', 'duration', 'created_at']

class ExamQuestionSerializer(serializers.ModelSerializer):
    question_detail = QuestionSerializer(source='question', read_only=True)
    
    class Meta:
        model = ExamQuestion
        fields = ['exam_question_id', 'exam', 'question', 'question_detail']