import jwt
from rest_framework import authentication, exceptions
from django.contrib.auth.models import AnonymousUser
from .models import User

class AuthenticatedUser:
    """包装自定义User模型以提供Django认证系统需要的属性"""
    def __init__(self, user):
        self.user = user
        self.user_id = user.user_id
        self.username = user.username
        self.role = user.role
        self.created_at = user.created_at
        
    @property
    def is_authenticated(self):
        return True
        
    @property
    def is_anonymous(self):
        return False
        
    @property
    def is_active(self):
        return True
        
    def __getattr__(self, name):
        # 代理到原始user对象
        return getattr(self.user, name)

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return None
        
        # 支持Bearer和Token两种格式
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        elif auth_header.startswith('Token '):
            token = auth_header.split(' ')[1]
        else:
            return None
        
        try:
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            if not user_id:
                raise exceptions.AuthenticationFailed('Invalid token')
            
            try:
                user = User.objects.get(user_id=user_id)
                # 包装用户对象以提供认证属性
                authenticated_user = AuthenticatedUser(user)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('User not found')
            
            return (authenticated_user, token)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
    
    def authenticate_header(self, request):
        return 'Bearer'