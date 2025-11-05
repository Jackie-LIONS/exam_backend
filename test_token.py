import requests
import json

# 先尝试登录获取token
passwords_to_try = ["admin123", "123456", "admin", "password"]

for password in passwords_to_try:
    login_data = {
        "username": "admin",
        "password": password
    }
    print(f"尝试密码: {password}")

    try:
        # 登录获取token
        login_response = requests.post('http://127.0.0.1:8000/api/users/login/', json=login_data)
        print(f"登录响应状态码: {login_response.status_code}")
        print(f"登录响应内容: {login_response.text}")
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result.get('token')
            print(f"获取到token: {token}")
            
            # 使用token调用dashboard API
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            dashboard_response = requests.get('http://127.0.0.1:8000/api/users/dashboard/stats/', headers=headers)
            print(f"Dashboard API响应状态码: {dashboard_response.status_code}")
            print(f"Dashboard API响应内容: {dashboard_response.text}")
            
            if dashboard_response.status_code == 200:
                dashboard_data = dashboard_response.json()
                print("Dashboard数据:")
                print(json.dumps(dashboard_data, indent=2, ensure_ascii=False))
                break  # 成功后退出循环
        else:
            print("登录失败")
            
    except Exception as e:
        print(f"错误: {e}")
    
    print("---")