import os
import requests

def send_to_pushdeer(title, content):
    push_key = os.environ.get('PUSHDEER_KEY')
    if not push_key:
        print("❌ Error: PUSHDEER_KEY is missing.")
        return

    url = "https://api2.pushdeer.com/message/push"
    payload = {
        "pushkey": push_key,
        "text": title,
        "desp": content,
        "type": "markdown"
    }
    
    try:
        resp = requests.post(url, data=payload, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        if result.get('code') == 0:
            print("✅ PushDeer 推送成功")
        else:
            print(f"❌ PushDeer 返回错误: {result}")
    except Exception as e:
        print(f"❌ 推送请求失败: {e}")
