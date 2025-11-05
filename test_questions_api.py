#!/usr/bin/env python3
"""
测试题目API返回的数据结构
"""

import requests
import json

def test_questions_api():
    """测试题目API"""
    base_url = "http://127.0.0.1:8000"
    
    # 1. 登录获取token
    login_data = {
        "username": "admin",
        "password": "123456"
    }
    
    print("1. 登录...")
    login_response = requests.post(f"{base_url}/api/users/login/", json=login_data)
    print(f"登录状态码: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print("登录失败")
        return
    
    login_data = login_response.json()
    print(f"登录响应: {login_data}")
    
    # 检查不同的token字段名
    token = login_data.get('access') or login_data.get('token') or login_data.get('access_token')
    if not token:
        print("未找到token")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 2. 获取题目列表
    print("\n2. 获取题目列表...")
    questions_response = requests.get(f"{base_url}/api/questions/", headers=headers)
    print(f"题目API状态码: {questions_response.status_code}")
    
    if questions_response.status_code == 200:
        data = questions_response.json()
        print(f"返回数据结构:")
        print(f"- 数据类型: {type(data)}")
        print(f"- 数据键: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        
        if 'data' in data:
            print(f"- data字段类型: {type(data['data'])}")
            print(f"- data字段长度: {len(data['data']) if isinstance(data['data'], list) else 'Not a list'}")
            if isinstance(data['data'], list) and len(data['data']) > 0:
                print(f"- 第一个题目结构: {list(data['data'][0].keys())}")
        
        print(f"\n完整响应数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"获取题目失败: {questions_response.text}")

if __name__ == "__main__":
    test_questions_api()