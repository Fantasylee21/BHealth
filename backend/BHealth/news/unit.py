import requests
import json

API_KEY = "sk-JqjB2sglQ94QK1E5MoX6NQUMRsH3GXtui7qg0XPm8ltRKe3U"
BASE_URL = "https://api.moonshot.cn/v1"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}


def ask(content):
    data = {
        "model": "moonshot-v1-8k",
        "messages": [
            {"role": "system",
             "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": content}
        ],
        "temperature": 0.3,
    }

    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=HEADERS,
        data=json.dumps(data)
    )

    if response.status_code == 200:
        completion = response.json()
        return completion['choices'][0]['message']['content']
    else:
        return "Error:", response.json()


# Example usage
if __name__ == "__main__":
    print(ask("给我讲个冷笑话"))
