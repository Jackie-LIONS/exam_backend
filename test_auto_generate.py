#!/usr/bin/env python
import requests
import json

# API基础URL
BASE_URL = "http://127.0.0.1:8000/api"

# 登录获取token
def login():
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/users/login/", json=login_data)
    if response.status_code == 200:
        token = response.json()["access"]
        print("登录成功")
        return token
    else:
        print("登录失败:", response.text)
        return None

# 测试自动组卷
def test_auto_generate(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 自动组卷数据
    auto_data = {
        "exam_name": "测试修复后的自动组卷",
        "start_time": "2024-01-20T10:00:00",
        "end_time": "2024-01-20T12:00:00", 
        "duration": 120,
        "easy_count": 2,
        "medium_count": 1,
        "hard_count": 2,
        "question_types": ["choice", "true_false", "fill_in_blank", "essay"]
    }
    
    print("发送自动组卷请求...")
    print("请求数据:", json.dumps(auto_data, indent=2, ensure_ascii=False))
    
    response = requests.post(f"{BASE_URL}/exams/generate/", json=auto_data, headers=headers)
    
    print(f"响应状态码: {response.status_code}")
    print("响应内容:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    
    if response.status_code == 201:
        exam_data = response.json()["exam"]
        exam_id = exam_data["exam_id"]
        
        # 获取生成的试卷题目
        print(f"\n获取试卷 {exam_id} 的题目...")
        questions_response = requests.get(f"{BASE_URL}/exams/{exam_id}/questions/", headers=headers)
        
        if questions_response.status_code == 200:
            questions = questions_response.json()
            print(f"试卷包含 {len(questions)} 道题目:")
            
            # 按题型和难度统计
            stats = {}
            for q in questions:
                question_type = q["question"]["question_type"]
                difficulty = q["question"]["difficulty_level"]
                
                if question_type not in stats:
                    stats[question_type] = {"easy": 0, "medium": 0, "hard": 0}
                stats[question_type][difficulty] += 1
            
            print("\n题目分布统计:")
            for qtype, difficulties in stats.items():
                print(f"{qtype}: 简单{difficulties['easy']}道, 中等{difficulties['medium']}道, 困难{difficulties['hard']}道")
                
            print("\n详细题目列表:")
            for i, q in enumerate(questions, 1):
                question = q["question"]
                print(f"{i}. [{question['question_type']}] [{question['difficulty_level']}] {question['content'][:50]}...")
        else:
            print("获取题目失败:", questions_response.text)
    else:
        print("自动组卷失败")

if __name__ == "__main__":
    token = login()
    if token:
        test_auto_generate(token)