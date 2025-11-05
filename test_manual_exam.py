# -*- coding: utf-8 -*-
import requests
import json

# 登录获取token
login_response = requests.post("http://127.0.0.1:8000/api/users/login/", json={
    "username": "admin",
    "password": "123456"
})

if login_response.status_code == 200:
    token = login_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 获取题目列表
    questions_response = requests.get("http://127.0.0.1:8000/api/questions/", headers=headers)
    if questions_response.status_code == 200:
        questions_data = questions_response.json()
        print("题目API响应结构:")
        print(json.dumps(questions_data, indent=2, ensure_ascii=False))
        
        # 检查是否是分页数据
        if isinstance(questions_data, dict) and 'data' in questions_data:
            questions = questions_data['data']
        else:
            questions = questions_data
            
        print(f"\n获取到 {len(questions)} 道题目")
        if questions and len(questions) > 0:
            print("第一道题目的结构:")
            print(json.dumps(questions[0], indent=2, ensure_ascii=False))
            
            # 测试手动组卷
            test_data = {
                "exam_name": "测试手动组卷",
                "duration": 60,
                "start_time": "2024-01-20T10:00:00",
                "end_time": "2024-01-20T11:00:00",
                "question_ids": [questions[0]["question_id"], questions[1]["question_id"]] if len(questions) > 1 else [questions[0]["question_id"]]
            }
            
            print("\n发送手动组卷请求:")
            print(json.dumps(test_data, indent=2, ensure_ascii=False))
            
            create_response = requests.post("http://127.0.0.1:8000/api/exams/create/", json=test_data, headers=headers)
            print(f"\n响应状态码: {create_response.status_code}")
            print("响应内容:")
            print(json.dumps(create_response.json(), indent=2, ensure_ascii=False))
        else:
            print("没有题目数据")
    else:
        print(f"获取题目失败: {questions_response.status_code}")
        print(questions_response.text)
else:
    print(f"登录失败: {login_response.status_code}")
    print(login_response.text)