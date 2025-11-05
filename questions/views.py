from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Question
from .serializers import QuestionSerializer
from users.authentication import JWTAuthentication

# 添加题目
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_question(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 获取所有题目
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_questions(request):
    # 获取分页参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 15))
    
    # 获取筛选参数
    question_type = request.GET.get('question_type')
    difficulty_level = request.GET.get('difficulty_level')
    
    # 构建查询条件
    queryset = Question.objects.all()
    
    # 添加筛选条件
    if question_type:
        queryset = queryset.filter(question_type=question_type)
    if difficulty_level:
        queryset = queryset.filter(difficulty_level=difficulty_level)
    
    # 计算偏移量
    offset = (page - 1) * page_size
    
    # 获取总数（应用筛选条件后的总数）
    total = queryset.count()
    
    # 获取分页数据
    questions = queryset[offset:offset + page_size]
    serializer = QuestionSerializer(questions, many=True)
    
    # 返回分页数据
    return Response({
        'data': serializer.data,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    })

# 获取指定题目
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_question(request, question_id):
    try:
        question = Question.objects.get(question_id=question_id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = QuestionSerializer(question)
    return Response(serializer.data)

# 更新题目
@api_view(['PUT', 'POST'])
@permission_classes([IsAuthenticated])
def update_question(request, question_id):
    try:
        question = Question.objects.get(question_id=question_id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = QuestionSerializer(question, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 删除题目
@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def delete_question(request, question_id):
    try:
        question = Question.objects.get(question_id=question_id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    question.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
