from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Exam, ExamQuestion
from .serializers import ExamSerializer, ExamQuestionSerializer
from questions.models import Question
import random

# 创建考试（手动组卷）
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_exam(request):
    # 获取题目ID列表
    question_ids = request.data.get('question_ids', [])
    
    # 创建考试基本信息
    exam_data = {
        'exam_name': request.data.get('exam_name'),
        'start_time': request.data.get('start_time'),
        'end_time': request.data.get('end_time'),
        'duration': request.data.get('duration')
    }
    
    serializer = ExamSerializer(data=exam_data)
    if serializer.is_valid():
        exam = serializer.save()
        
        # 添加选中的题目到考试
        if question_ids:
            for question_id in question_ids:
                try:
                    question = Question.objects.get(question_id=question_id)
                    ExamQuestion.objects.create(exam=exam, question=question)
                except Question.DoesNotExist:
                    continue
        
        # 返回包含题目数量的考试信息
        exam_data = ExamSerializer(exam).data
        exam_data['question_count'] = ExamQuestion.objects.filter(exam=exam).count()
        
        return Response(exam_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 获取所有考试
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exams(request):
    # 获取分页参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 15))
    
    # 计算偏移量
    offset = (page - 1) * page_size
    
    # 获取总数
    total = Exam.objects.count()
    
    # 获取分页数据
    exams = Exam.objects.all()[offset:offset + page_size]
    serializer = ExamSerializer(exams, many=True)
    
    # 为每个考试添加题目数量
    exam_data = serializer.data
    for exam in exam_data:
        exam_id = exam['exam_id']
        question_count = ExamQuestion.objects.filter(exam_id=exam_id).count()
        exam['question_count'] = question_count
    
    # 返回分页数据
    return Response({
        'data': exam_data,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    })

# 获取单个考试
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exam(request, exam_id):
    try:
        exam = Exam.objects.get(exam_id=exam_id)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExamSerializer(exam)
    return Response(serializer.data)

# 更新考试
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_exam(request, exam_id):
    try:
        exam = Exam.objects.get(exam_id=exam_id)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExamSerializer(exam, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 删除考试
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_exam(request, exam_id):
    try:
        exam = Exam.objects.get(exam_id=exam_id)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    exam.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# 添加题目到考试
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_question_to_exam(request):
    exam_id = request.data.get('exam')
    question_id = request.data.get('question')
    
    try:
        exam = Exam.objects.get(exam_id=exam_id)
        question = Question.objects.get(question_id=question_id)
    except (Exam.DoesNotExist, Question.DoesNotExist):
        return Response({"error": "考试或题目不存在"}, status=status.HTTP_404_NOT_FOUND)
    
    exam_question = ExamQuestion(exam=exam, question=question)
    exam_question.save()
    
    serializer = ExamQuestionSerializer(exam_question)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# 获取考试的所有题目
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exam_questions(request, exam_id):
    try:
        exam = Exam.objects.get(exam_id=exam_id)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    exam_questions = ExamQuestion.objects.filter(exam=exam)
    serializer = ExamQuestionSerializer(exam_questions, many=True)
    return Response(serializer.data)

# 自动组卷
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_exam_paper(request):
    # 获取考试基本信息
    exam_name = request.data.get('exam_name')
    start_time = request.data.get('start_time')
    end_time = request.data.get('end_time')
    duration = request.data.get('duration')
    
    # 获取题目配置
    easy_count = int(request.data.get('easy_count', 0))
    medium_count = int(request.data.get('medium_count', 0))
    hard_count = int(request.data.get('hard_count', 0))
    question_types = request.data.get('question_types', [])
    
    # 创建考试
    exam_data = {
        'exam_name': exam_name,
        'start_time': start_time,
        'end_time': end_time,
        'duration': duration
    }
    
    serializer = ExamSerializer(data=exam_data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    exam = serializer.save()
    
    # 为每种题型按难度分布生成题目
    selected_questions = []
    total_questions = 0
    
    # 遍历每种题型
    for question_type in question_types:
        # 获取当前题型不同难度的题目
        easy_questions = list(Question.objects.filter(
            difficulty_level='easy', 
            question_type=question_type
        ))
        medium_questions = list(Question.objects.filter(
            difficulty_level='medium', 
            question_type=question_type
        ))
        hard_questions = list(Question.objects.filter(
            difficulty_level='hard', 
            question_type=question_type
        ))
        
        # 检查当前题型的题目数量是否足够
        if easy_count > 0 and len(easy_questions) < easy_count:
            return Response({
                "error": f"{question_type}类型的简单题目不足，需要 {easy_count} 道，实际只有 {len(easy_questions)} 道"
            }, status=status.HTTP_400_BAD_REQUEST)
        if medium_count > 0 and len(medium_questions) < medium_count:
            return Response({
                "error": f"{question_type}类型的中等题目不足，需要 {medium_count} 道，实际只有 {len(medium_questions)} 道"
            }, status=status.HTTP_400_BAD_REQUEST)
        if hard_count > 0 and len(hard_questions) < hard_count:
            return Response({
                "error": f"{question_type}类型的困难题目不足，需要 {hard_count} 道，实际只有 {len(hard_questions)} 道"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 为当前题型随机选择题目
        if easy_count > 0:
            selected_questions.extend(random.sample(easy_questions, easy_count))
            total_questions += easy_count
        if medium_count > 0:
            selected_questions.extend(random.sample(medium_questions, medium_count))
            total_questions += medium_count
        if hard_count > 0:
            selected_questions.extend(random.sample(hard_questions, hard_count))
            total_questions += hard_count
    
    # 添加题目到考试
    for question in selected_questions:
        ExamQuestion.objects.create(exam=exam, question=question)
    
    # 返回包含题目数量的考试信息
    exam_data = ExamSerializer(exam).data
    exam_data['question_count'] = total_questions
    
    return Response({
        "message": f"成功自动生成试卷，包含 {total_questions} 道题目（每种题型：简单{easy_count}道，中等{medium_count}道，困难{hard_count}道）",
        "exam": exam_data
    }, status=status.HTTP_201_CREATED)

# 从考试中移除题目
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_question_from_exam(request, exam_question_id):
    try:
        exam_question = ExamQuestion.objects.get(exam_question_id=exam_question_id)
    except ExamQuestion.DoesNotExist:
        return Response({"error": "考试题目不存在"}, status=status.HTTP_404_NOT_FOUND)
    
    exam_question.delete()
    return Response({"message": "题目移除成功"}, status=status.HTTP_204_NO_CONTENT)
