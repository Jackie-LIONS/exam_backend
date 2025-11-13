

<center><img src="https://img-blog.csdnimg.cn/299da6849a844e6881a91ce15d16239c.gif#pic_center" alt="权限管理"></center>

> 项目定制业务：**前端、后端(Python、Java、C#、PHP)、算法（深度学习、机器学习）、大数据（Hadoop、hive、spark）、小程序等项目**，
> 无论是**商用**还是**学校项目（毕业设计、课程设计等）**，都可咨询，价格合理，服务周全！
> 如果你有需要，添加vx：**732708009**，手把手帮你把项目运行起来
# 一.🦁 项目概述

基于Django开发的智慧校园考试系统后端API，采用前后端分离架构，提供RESTful风格接口，涵盖用户管理、题库管理、考试管理和成绩管理等核心功能模块。首先，用户管理模块支持学生和管理员两种角色，提供用户注册与登录（JWT认证）、个人信息管理。其次，题库管理模块支持多种试题类型，如单选题、判断题、填空题、简答题，实现试题的CRUD操作、智能组卷算法、试题分类标签管理及难度系数设置。然后，考试管理模块涵盖考试创建、考生报名与审核、在线考试等功能，提供考试场次管理。最后，成绩管理模块实现了自动评分（客观题）、成绩统计分析、提供成绩查询、成绩分布可视化以及错题分析和历史成绩对比等功能。
## 1.1 技术栈

- Python 3.8+
- Django 4.2
- Django REST Framework
- MySQL

## 1.2 安装与运行

1. 克隆项目
2. 安装依赖：`pip install -r requirements.txt`
3. 配置数据库：修改`settings.py`中的数据库配置
4. 迁移数据库：`python manage.py migrate`
5. 运行服务器：`python manage.py runserver`

# 二.🦁 演示系统流程
## 2.1 管理员端

1. 登录

![1](https://i-blog.csdnimg.cn/img_convert/b08112660a3e4b45822cc72e7dd27a07.png)
2. 仪表板
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e687f1f87bc349f3a61f40eb22b4e375.png)
3. 用户管理
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/7fec790af7a0439da1a01f4597a96bac.png)
4. 题库管理
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/36a766d1fda94e6489c2f170d1086bff.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/4f7bb2801ffc47eaa099af3dea2465ff.png)
5. 考试管理
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d2ffc6fccd284473bf27d30038c65236.png)
6. 试卷管理
- 手动组卷
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/67291b8c15454ccf80a332880094e00d.png)
- 自动组卷
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/04dc4666f67d4f6b9764a3428f0583c2.png)
7. 成绩管理
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/bf11c2a4cbb140c281014662f3bf16a9.png)
## 2.2 学生端
1. 首页
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/2d6fcab29e374ca0a7d4fc619782524f.png)
2. 考试列表
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f406e92c13454392af87b9feb86abdb4.png)
3. 查看成绩
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d6cf2fc2639648b2bfb581ad956dd540.png)
4. 个人中心
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f713ad15df2e4aff9ad00e207bb54417.png)
# 三.🦁 API接口文档

## 3.1 用户管理

1. 注册用户
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

2. 用户登录

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

3. 获取当前用户信息

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

4. 获取所有用户

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

5.  获取特定用户

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

6. 更新用户

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

7. 删除用户

- URL: `/api/users/{user_id}/delete/`
- 方法: DELETE
- 请求头: `Authorization: Bearer {token}`
- 响应: 204 No Content

## 3.2 题库管理

1. 添加题目

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

2. 获取所有题目

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

3. 获取特定题目

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

4. 更新题目

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

5. 删除题目

- URL: `/api/questions/delete/{question_id}/`
- 方法: DELETE
- 请求头: `Authorization: Bearer {token}`
- 响应: 204 No Content

## 3.3 考试管理

1. 创建考试

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

2. 获取所有考试

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

3. 获取特定考试

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

4. 更新考试

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

5. 删除考试

- URL: `/api/exams/delete/{exam_id}/`
- 方法: DELETE
- 请求头: `Authorization: Bearer {token}`
- 响应: 204 No Content

6. 添加题目到考试

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

7. 获取考试的所有题目

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

8. 自动组卷

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

## 3.4 成绩管理

1. 添加成绩

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

2. 获取用户成绩

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

3. 获取考试成绩

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

4. 获取历史考试记录

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






-- --
![在这里插入图片描述](https://img-blog.csdnimg.cn/59e6298ecc134fbeb947b1b24ecfd48a.gif#pic_center)

<h2><center>🦁 其它优质专栏推荐 🦁</center></h2>

>:star2:[《Java核心系列（修炼内功，无上心法)》](https://blog.csdn.net/m0_58847451/category_12280615.html?spm=1001.2014.3001.5482): **主要是JDK源码的核心讲解，几乎每篇文章都过万字，让你详细掌握每一个知识点！**

>:star2: [《springBoot 源码剥析核心系列》](https://blog.csdn.net/m0_58847451/category_12226203.html?spm=1001.2014.3001.5482)：**一些场景的Springboot源码剥析以及常用Springboot相关知识点解读**


**欢迎加入狮子的社区**：『[Lion-编程进阶之路](https://bbs.csdn.net/forums/lion-society?spm=1001.2014.3001.6682)』，日常收录优质好文

**更多文章可持续关注上方🦁的博客，2025咱们顶峰相见！**
