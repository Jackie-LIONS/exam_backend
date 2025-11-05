from rest_framework import serializers
from .models import Score, ExamHistory
from users.serializers import UserSerializer
from exams.serializers import ExamSerializer

class ScoreSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    exam_detail = ExamSerializer(source='exam', read_only=True)
    
    class Meta:
        model = Score
        fields = ['score_id', 'user', 'exam', 'score', 'created_at', 'user_detail', 'exam_detail']
        extra_kwargs = {
            'user': {'write_only': True},
            'exam': {'write_only': True},
        }

class ExamHistorySerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    exam_detail = ExamSerializer(source='exam', read_only=True)
    
    class Meta:
        model = ExamHistory
        fields = ['history_id', 'user', 'exam', 'score', 'completed_at', 'user_detail', 'exam_detail']
        extra_kwargs = {
            'user': {'write_only': True},
            'exam': {'write_only': True},
        }