# 智慧校园考试系统后端API文档

## 项目概述
智慧校园考试系统后端API，基于Django REST Framework开发，提供用户管理、题库管理、考试管理、成绩管理等功能。

## 技术栈
- Python 3.8+
- Django 4.2
- Django REST Framework
- MySQL

## 安装与运行
1. 克隆项目
2. 安装依赖：`pip install -r requirements.txt`
3. 配置数据库：修改`settings.py`中的数据库配置
4. 迁移数据库：`python manage.py migrate`
5. 运行服务器：`python manage.py runserver`

## API接口文档

### 用户管理

#### 注册用户
- URL: `/api/users/register/`
- 方法: POST
- 请求体:
  ```json
  {
    "username": "用户名",
    "password": "密码",
    "role": "admin或student"
  }
  ```
- 响应:
  ```json
  {
    "user_id": 1,
    "username": "用户名",
    "role": "admin或student",
    "created_at": "创建时间"
  }
  ```

#### 用户登录
- URL: `/api/users/login/`
- 方法: POST
- 请求体:
  ```json
  {
    "username": "用户名",
    "password": "密码"
  }
  ```
- 响应:
  ```json
  {
    "token": "JWT令牌",
    "user": {
      "user_id": 1,
      "username": "用户名",
      "role": "admin或student"
    }
  }
  ```

#### 获取当前用户信息
- URL: `/api/users/current/`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  {
    "user_id": 1,
    "username": "用户名",
    "role": "admin或student",
    "created_at": "创建时间"
  }
  ```

#### 获取所有用户
- URL: `/api/users/`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  [
    {
      "user_id": 1,
      "username": "用户名",
      "role": "admin或student",
      "created_at": "创建时间"
    }
  ]
  ```

#### 获取特定用户
- URL: `/api/users/{user_id}/`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  {
    "user_id": 1,
    "username": "用户名",
    "role": "admin或student",
    "created_at": "创建时间"
  }
  ```

#### 更新用户
- URL: `/api/users/{user_id}/update/`
- 方法: PUT
- 请求头: `Authorization: Bearer {token}`
- 请求体:
  ```json
  {
    "username": "新用户名",
    "password": "新密码",
    "role": "新角色"
  }
  ```
- 响应:
  ```json
  {
    "user_id": 1,
    "username": "新用户名",
    "role": "新角色",
    "created_at": "创建时间"
  }
  ```

#### 删除用户
- URL: `/api/users/{user_id}/delete/`
- 方法: DELETE
- 请求头: `Authorization: Bearer {token}`
- 响应: 204 No Content

### 题库管理

#### 添加题目
- URL: `/api/questions/add/`
- 方法: POST
- 请求头: `Authorization: Bearer {token}`
- 请求体:
  ```json
  {
    "content": "题目内容",
    "question_type": "choice/true_false/fill_in_blank/essay",
    "difficulty_level": "easy/medium/hard"
  }
  ```
- 响应:
  ```json
  {
    "question_id": 1,
    "content": "题目内容",
    "question_type": "choice/true_false/fill_in_blank/essay",
    "difficulty_level": "easy/medium/hard",
    "created_at": "创建时间"
  }
  ```

#### 获取所有题目
- URL: `/api/questions/`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  [
    {
      "question_id": 1,
      "content": "题目内容",
      "question_type": "choice/true_false/fill_in_blank/essay",
      "difficulty_level": "easy/medium/hard",
      "created_at": "创建时间"
    }
  ]
  ```

#### 获取特定题目
- URL: `/api/questions/get/{question_id}/`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  {
    "question_id": 1,
    "content": "题目内容",
    "question_type": "choice/true_false/fill_in_blank/essay",
    "difficulty_level": "easy/medium/hard",
    "created_at": "创建时间"
  }
  ```

#### 更新题目
- URL: `/api/questions/update/{question_id}/`
- 方法: PUT
- 请求头: `Authorization: Bearer {token}`
- 请求体:
  ```json
  {
    "content": "新题目内容",
    "question_type": "新题目类型",
    "difficulty_level": "新难度级别"
  }
  ```
- 响应:
  ```json
  {
    "question_id": 1,
    "content": "新题目内容",
    "question_type": "新题目类型",
    "difficulty_level": "新难度级别",
    "created_at": "创建时间"
  }
  ```

#### 删除题目
- URL: `/api/questions/delete/{question_id}/`
- 方法: DELETE
- 请求头: `Authorization: Bearer {token}`
- 响应: 204 No Content

### 考试管理

#### 创建考试
- URL: `/api/exams/create/`
- 方法: POST
- 请求头: `Authorization: Bearer {token}`
- 请求体:
  ```json
  {
    "exam_name": "考试名称",
    "start_time": "开始时间",
    "end_time": "结束时间",
    "duration": 120
  }
  ```
- 响应:
  ```json
  {
    "exam_id": 1,
    "exam_name": "考试名称",
    "start_time": "开始时间",
    "end_time": "结束时间",
    "duration": 120,
    "created_at": "创建时间"
  }
  ```

#### 获取所有考试
- URL: `/api/exams/`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  [
    {
      "exam_id": 1,
      "exam_name": "考试名称",
      "start_time": "开始时间",
      "end_time": "结束时间",
      "duration": 120,
      "created_at": "创建时间"
    }
  ]
  ```

#### 获取特定考试
- URL: `/api/exams/get/{exam_id}/`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  {
    "exam_id": 1,
    "exam_name": "考试名称",
    "start_time": "开始时间",
    "end_time": "结束时间",
    "duration": 120,
    "created_at": "创建时间"
  }
  ```

#### 更新考试
- URL: `/api/exams/update/{exam_id}/`
- 方法: PUT
- 请求头: `Authorization: Bearer {token}`
- 请求体:
  ```json
  {
    "exam_name": "新考试名称",
    "start_time": "新开始时间",
    "end_time": "新结束时间",
    "duration": 150
  }
  ```
- 响应:
  ```json
  {
    "exam_id": 1,
    "exam_name": "新考试名称",
    "start_time": "新开始时间",
    "end_time": "新结束时间",
    "duration": 150,
    "created_at": "创建时间"
  }
  ```

#### 删除考试
- URL: `/api/exams/delete/{exam_id}/`
- 方法: DELETE
- 请求头: `Authorization: Bearer {token}`
- 响应: 204 No Content

#### 添加题目到考试
- URL: `/api/exams/add_question/`
- 方法: POST
- 请求头: `Authorization: Bearer {token}`
- 请求体:
  ```json
  {
    "exam": 1,
    "question": 1
  }
  ```
- 响应:
  ```json
  {
    "exam_question_id": 1,
    "exam": 1,
    "question": 1,
    "question_detail": {
      "question_id": 1,
      "content": "题目内容",
      "question_type": "题目类型",
      "difficulty_level": "难度级别",
      "created_at": "创建时间"
    }
  }
  ```

#### 获取考试的所有题目
- URL: `/api/exams/questions/{exam_id}/`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  [
    {
      "exam_question_id": 1,
      "exam": 1,
      "question": 1,
      "question_detail": {
        "question_id": 1,
        "content": "题目内容",
        "question_type": "题目类型",
        "difficulty_level": "难度级别",
        "created_at": "创建时间"
      }
    }
  ]
  ```

#### 自动组卷
- URL: `/api/exams/generate_paper/`
- 方法: POST
- 请求头: `Authorization: Bearer {token}`
- 请求体:
  ```json
  {
    "exam_id": 1,
    "easy_count": 5,
    "medium_count": 3,
    "hard_count": 2
  }
  ```
- 响应:
  ```json
  {
    "message": "成功添加 10 道题目到考试"
  }
  ```

### 成绩管理

#### 添加成绩
- URL: `/api/scores/add/`
- 方法: POST
- 请求头: `Authorization: Bearer {token}`
- 请求体:
  ```json
  {
    "user": 1,
    "exam": 1,
    "score": 85
  }
  ```
- 响应:
  ```json
  {
    "score_id": 1,
    "user": 1,
    "exam": 1,
    "score": 85,
    "created_at": "创建时间",
    "user_detail": {
      "user_id": 1,
      "username": "用户名",
      "role": "角色",
      "created_at": "创建时间"
    },
    "exam_detail": {
      "exam_id": 1,
      "exam_name": "考试名称",
      "start_time": "开始时间",
      "end_time": "结束时间",
      "duration": 120,
      "created_at": "创建时间"
    }
  }
  ```

#### 获取用户成绩
- URL: `/api/scores/user/{user_id}/`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  [
    {
      "score_id": 1,
      "user": 1,
      "exam": 1,
      "score": 85,
      "created_at": "创建时间",
      "user_detail": {
        "user_id": 1,
        "username": "用户名",
        "role": "角色",
        "created_at": "创建时间"
      },
      "exam_detail": {
        "exam_id": 1,
        "exam_name": "考试名称",
        "start_time": "开始时间",
        "end_time": "结束时间",
        "duration": 120,
        "created_at": "创建时间"
      }
    }
  ]
  ```

#### 获取考试成绩
- URL: `/api/scores/exam/{exam_id}/`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  [
    {
      "score_id": 1,
      "user": 1,
      "exam": 1,
      "score": 85,
      "created_at": "创建时间",
      "user_detail": {
        "user_id": 1,
        "username": "用户名",
        "role": "角色",
        "created_at": "创建时间"
      },
      "exam_detail": {
        "exam_id": 1,
        "exam_name": "考试名称",
        "start_time": "开始时间",
        "end_time": "结束时间",
        "duration": 120,
        "created_at": "创建时间"
      }
    }
  ]
  ```

#### 获取历史考试记录
- URL: `/api/scores/history/{user_id}/`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  [
    {
      "history_id": 1,
      "user": 1,
      "exam": 1,
      "score": 85,
      "completed_at": "完成时间",
      "user_detail": {
        "user_id": 1,
        "username": "用户名",
        "role": "角色",
        "created_at": "创建时间"
      },
      "exam_detail": {
        "exam_id": 1,
        "exam_name": "考试名称",
        "start_time": "开始时间",
        "end_time": "结束时间",
        "duration": 120,
        "created_at": "创建时间"
      }
    }
  ]
  ```