from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Score, ExamHistory
from .serializers import ScoreSerializer, ExamHistorySerializer
from users.models import User
from exams.models import Exam, ExamQuestion
from questions.models import Question
import json

# 添加成绩
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_score(request):
    serializer = ScoreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 获取某个学生的成绩
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_scores(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    scores = Score.objects.filter(user=user)
    serializer = ScoreSerializer(scores, many=True)
    return Response(serializer.data)

# 获取考试成绩
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exam_scores(request, exam_id):
    try:
        exam = Exam.objects.get(exam_id=exam_id)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    scores = Score.objects.filter(exam=exam)
    serializer = ScoreSerializer(scores, many=True)
    return Response(serializer.data)

# 获取所有成绩
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_scores(request):
    # 获取分页参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 15))
    
    # 计算偏移量
    offset = (page - 1) * page_size
    
    # 获取总数
    total = Score.objects.count()
    
    # 获取分页数据
    scores = Score.objects.all()[offset:offset + page_size]
    serializer = ScoreSerializer(scores, many=True)
    
    # 返回分页数据
    return Response({
        'data': serializer.data,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    })

# 获取历史考试记录
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exam_history(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    history = ExamHistory.objects.filter(user=user)
    serializer = ExamHistorySerializer(history, many=True)
    return Response(serializer.data)

# 提交考试答案并计算成绩
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_exam(request):
    try:
        user_id = request.data.get('user_id')
        exam_id = request.data.get('exam_id')
        answers = request.data.get('answers', [])
        
        # 验证用户和考试是否存在
        try:
            user = User.objects.get(user_id=user_id)
            exam = Exam.objects.get(exam_id=exam_id)
        except (User.DoesNotExist, Exam.DoesNotExist):
            return Response({'error': '用户或考试不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 获取考试题目
        exam_questions = ExamQuestion.objects.filter(exam=exam)
        total_questions = exam_questions.count()
        correct_answers = 0
        
        # 计算得分
        for answer in answers:
            question_id = answer.get('question_id')
            selected_options = answer.get('selected_options', [])
            
            try:
                question = Question.objects.get(question_id=question_id)
                
                if question.question_type == 'choice':
                    # 处理选择题
                    options = question.options
                    if isinstance(options, str):
                        options = json.loads(options)
                    
                    # 获取正确答案
                    correct_option_indices = []
                    for i, option in enumerate(options):
                        if option.get('is_correct', False):
                            correct_option_indices.append(str(i))
                    
                    # 比较用户答案和正确答案
                    user_answers = [str(opt) for opt in selected_options]
                    if set(user_answers) == set(correct_option_indices):
                        correct_answers += 1
                        
            except Question.DoesNotExist:
                continue
        
        # 计算得分百分比
        score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # 保存成绩记录
        score_record = Score.objects.create(
            user=user,
            exam=exam,
            score=score
        )
        
        # 保存考试历史记录
        ExamHistory.objects.create(
            user=user,
            exam=exam,
            score=score
        )
        
        return Response({
            'score': score,
            'correct_answers': correct_answers,
            'total_questions': total_questions,
            'message': '考试提交成功'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
