#!/usr/bin/env python3
"""
简单测试后端连接
"""

import requests

def test_backend():
    """测试后端连接"""
    base_url = "http://127.0.0.1:8000"
    
    # 测试根路径
    print("1. 测试用户API根路径...")
    try:
        response = requests.get(f"{base_url}/api/users/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text[:200]}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试登录路径
    print("\n2. 测试登录路径...")
    try:
        response = requests.post(f"{base_url}/api/users/login/", json={})
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text[:200]}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    test_backend()