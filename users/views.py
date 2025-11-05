from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from questions.models import Question
from exams.models import Exam
from scores.models import Score
from django.utils import timezone
from django.db.models import Avg, Count
import jwt
import datetime
import hashlib

# 用户注册
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 用户登录
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    # 验证密码（支持MD5哈希和明文）
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    if user.password != password and user.password != hashed_password:
        return Response({'error': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # 生成JWT token
    payload = {
        'user_id': user.user_id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, 'secret_key', algorithm='HS256')
    
    return Response({
        'token': token,
        'user': UserSerializer(user).data
    })

# 获取当前用户信息
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

# 获取所有用户
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    # 获取分页参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 15))
    
    # 计算偏移量
    offset = (page - 1) * page_size
    
    # 获取总数
    total = User.objects.count()
    
    # 获取分页数据
    users = User.objects.all()[offset:offset + page_size]
    serializer = UserSerializer(users, many=True)
    
    # 返回分页数据
    return Response({
        'data': serializer.data,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    })

# 获取指定用户
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user)
    return Response(serializer.data)

# 更新用户
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 删除用户
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# 获取Dashboard统计数据
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_stats(request):
    try:
        # 获取学生总数
        total_students = User.objects.filter(role='student').count()
        
        # 获取题库总量
        total_questions = Question.objects.count()
        
        # 获取进行中考试数量（当前时间在考试开始和结束时间之间）
        now = timezone.now()
        ongoing_exams = Exam.objects.filter(
            start_time__lte=now,
            end_time__gte=now
        ).count()
        
        # 获取平均分数
        avg_score_data = Score.objects.aggregate(avg_score=Avg('score'))
        average_score = round(avg_score_data['avg_score'] or 0, 1)
        
        # 获取最近考试列表（最近5场考试）
        recent_exams = []
        exams = Exam.objects.order_by('-created_at')[:5]
        
        for exam in exams:
            # 获取参与人数
            participants = Score.objects.filter(exam=exam).count()
            
            # 判断考试状态
            if now < exam.start_time:
                status_text = '未开始'
            elif now > exam.end_time:
                status_text = '已结束'
            else:
                status_text = '进行中'
            
            recent_exams.append({
                'id': exam.exam_id,
                'name': exam.exam_name,
                'startTime': exam.start_time.strftime('%Y-%m-%d %H:%M'),
                'participants': participants,
                'status': status_text
            })
        
        # 获取考试统计数据（最近7天的考试数量）
        exam_stats = []
        for i in range(7):
            date = (now - datetime.timedelta(days=i)).date()
            exam_count = Exam.objects.filter(created_at__date=date).count()
            exam_stats.append({
                'date': date.strftime('%m-%d'),
                'count': exam_count
            })
        exam_stats.reverse()  # 按时间正序排列
        
        # 获取成绩分布数据
        score_distribution = []
        score_ranges = [
            {'range': '0-60', 'min': 0, 'max': 60},
            {'range': '60-70', 'min': 60, 'max': 70},
            {'range': '70-80', 'min': 70, 'max': 80},
            {'range': '80-90', 'min': 80, 'max': 90},
            {'range': '90-100', 'min': 90, 'max': 100}
        ]
        
        for range_data in score_ranges:
            count = Score.objects.filter(
                score__gte=range_data['min'],
                score__lt=range_data['max'] if range_data['max'] < 100 else 101
            ).count()
            score_distribution.append({
                'range': range_data['range'],
                'count': count
            })

        return Response({
            'totalStudents': total_students,
            'totalQuestions': total_questions,
            'ongoingExams': ongoing_exams,
            'averageScore': average_score,
            'recentExams': recent_exams,
            'examStats': exam_stats,
            'scoreDistribution': score_distribution
        })
        
    except Exception as e:
        return Response(
            {'error': f'获取统计数据失败: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# 获取学生个人统计数据
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_stats(request):
    """获取学生个人统计数据"""
    try:
        # 从认证中获取用户对象
        user = request.user
        if not user or not user.is_authenticated:
            return Response({'error': '用户未认证'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 获取原始用户对象（如果是AuthenticatedUser包装类）
        if hasattr(user, 'user'):
            actual_user = user.user
        else:
            actual_user = user
        
        # 获取学生已完成的不同考试数量
        completed_exams = Score.objects.filter(user=actual_user).values('exam').distinct().count()
        
        # 获取学生的平均成绩
        avg_score_data = Score.objects.filter(user=actual_user).aggregate(avg_score=Avg('score'))
        average_score = round(avg_score_data['avg_score'] or 0, 1)
        
        # 获取学生的考试完成率
        # 计算总的考试数量
        total_exams = Exam.objects.count()
        completion_rate = round((completed_exams / total_exams * 100) if total_exams > 0 else 0, 1)
        
        # 获取学生最近的考试成绩（最近5次）
        recent_scores = []
        scores = Score.objects.filter(user=actual_user).order_by('-created_at')[:5]
        
        for score in scores:
            recent_scores.append({
                'id': score.score_id,
                'examName': score.exam.exam_name,
                'score': score.score,
                'totalScore': 100,  # 假设总分为100
                'date': score.created_at.strftime('%Y-%m-%d %H:%M'),
                'status': '已完成'
            })
        
        # 获取即将到来的考试（未开始的考试）
        upcoming_exams = []
        # 确保使用当前时间进行比较，并且只获取真正未来的考试
        current_time = timezone.now()
        exams = Exam.objects.filter(start_time__gt=current_time).order_by('start_time')[:5]
        
        for exam in exams:
            # 将UTC时间转换为本地时间显示
            local_start_time = exam.start_time.astimezone()
            local_end_time = exam.end_time.astimezone()
            
            upcoming_exams.append({
                'id': exam.exam_id,
                'name': exam.exam_name,
                'startTime': local_start_time.strftime('%Y-%m-%d %H:%M'),
                'endTime': local_end_time.strftime('%Y-%m-%d %H:%M'),
                'duration': exam.duration,
                'status': '未开始'
            })

        return Response({
            'completedExams': completed_exams,
            'averageScore': average_score,
            'completionRate': completion_rate,
            'recentScores': recent_scores,
            'upcomingExams': upcoming_exams
        })
        
    except Exception as e:
        return Response(
            {'error': f'获取学生统计数据失败: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
