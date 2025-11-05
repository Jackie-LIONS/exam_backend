# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime, timedelta

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
        
        # 检查是否是分页数据
        if isinstance(questions_data, dict) and 'data' in questions_data:
            questions = questions_data['data']
        else:
            questions = questions_data
            
        print(f"获取到 {len(questions)} 道题目")
        
        if questions and len(questions) > 0:
            # 使用正确的日期格式测试手动组卷
            now = datetime.now()
            start_time = now + timedelta(hours=1)
            end_time = start_time + timedelta(hours=2)
            
            test_data = {
                "exam_name": "测试修复后的手动组卷",
                "duration": 60,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "question_ids": [questions[0]["question_id"], questions[1]["question_id"]] if len(questions) > 1 else [questions[0]["question_id"]]
            }
            
            print("\n发送修复后的手动组卷请求:")
            print(json.dumps(test_data, indent=2, ensure_ascii=False))
            
            create_response = requests.post("http://127.0.0.1:8000/api/exams/create/", json=test_data, headers=headers)
            print(f"\n响应状态码: {create_response.status_code}")
            print("响应内容:")
            try:
                response_json = create_response.json()
                print(json.dumps(response_json, indent=2, ensure_ascii=False))
                
                if create_response.status_code == 201:
                    print("\n✅ 手动组卷功能修复成功！")
                else:
                    print(f"\n❌ 手动组卷仍有问题，状态码: {create_response.status_code}")
            except:
                print("响应不是有效的JSON格式:")
                print(create_response.text)
        else:
            print("没有题目数据")
    else:
        print(f"获取题目失败: {questions_response.status_code}")
        print(questions_response.text)
else:
    print(f"登录失败: {login_response.status_code}")
    print(login_response.text)