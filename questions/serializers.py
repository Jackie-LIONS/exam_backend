from rest_framework import serializers
from .models import Question
import json

class QuestionSerializer(serializers.ModelSerializer):
    # 兼容前端的question_text字段
    question_text = serializers.CharField(write_only=True, required=False)
    # 统一的正确答案字段
    correct_answer = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['question_id', 'content', 'question_type', 'difficulty_level', 'choice_type', 
                 'options', 'true_false_answer', 'fill_answer', 'essay_answer', 'created_at', 'question_text', 'correct_answer']
        extra_kwargs = {
            'content': {'required': False},
            'fill_answer': {'allow_blank': True},
            'essay_answer': {'allow_blank': True},
        }
    
    def get_correct_answer(self, obj):
        """根据题目类型返回相应的正确答案"""
        if obj.question_type == 'choice':
            if obj.options:
                # 处理带有is_correct标记的格式
                if isinstance(obj.options, list) and len(obj.options) > 0 and isinstance(obj.options[0], dict) and 'is_correct' in obj.options[0]:
                    for option in obj.options:
                        if option.get('is_correct'):
                            return option.get('option_text', '')
                # 处理简单键值对格式（这种格式需要额外的答案字段，暂时返回提示）
                else:
                    return "请查看选项"
            return "无选项"
        elif obj.question_type == 'true_false':
            if obj.true_false_answer is not None:
                return "正确" if obj.true_false_answer else "错误"
            return "未设置答案"
        elif obj.question_type == 'fill_in_blank':
            return obj.fill_answer or "未设置答案"
        elif obj.question_type == 'essay':
            return obj.essay_answer or "未设置答案"
        return ""
    
    def validate(self, data):
        # 处理question_text到content的映射
        if 'question_text' in data and data['question_text']:
            data['content'] = data.pop('question_text')
        
        # 确保content字段存在
        if 'content' not in data or not data['content']:
            raise serializers.ValidationError({'content': 'This field is required.'})
        
        # 设置默认难度级别
        if 'difficulty_level' not in data:
            data['difficulty_level'] = 'medium'
        
        # 根据题目类型验证相应的答案字段
        question_type = data.get('question_type')
        
        if question_type == 'choice':
            if not data.get('options'):
                raise serializers.ValidationError({'options': 'Choice questions must have options.'})
            if not data.get('choice_type'):
                data['choice_type'] = 'single'  # 默认单选
        
        elif question_type == 'true_false':
            if data.get('true_false_answer') is None:
                raise serializers.ValidationError({'true_false_answer': 'True/False questions must have an answer.'})
        
        elif question_type == 'fill_in_blank':
            if not data.get('fill_answer'):
                raise serializers.ValidationError({'fill_answer': 'Fill-in-blank questions must have an answer.'})
        
        elif question_type == 'essay':
            if not data.get('essay_answer'):
                raise serializers.ValidationError({'essay_answer': 'Essay questions must have a reference answer.'})
        
        return data