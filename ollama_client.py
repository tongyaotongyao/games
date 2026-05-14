import requests
import json

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, model, prompt, stream=False, max_tokens=1024):
        """
        调用Ollama生成接口
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.7
            }
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"请求失败: {response.status_code}")
    
    def chat(self, model, messages, stream=False):
        """
        调用Ollama聊天接口
        """
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"请求失败: {response.status_code}")
    
    def list_models(self):
        """
        列出已安装的模型
        """
        url = f"{self.base_url}/api/tags"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"请求失败: {response.status_code}")

if __name__ == "__main__":
    client = OllamaClient()
    
    print("检查Ollama服务...")
    try:
        models = client.list_models()
        print(f"已安装的模型: {[m['name'] for m in models['models']]}")
        
        print("\n测试生成功能...")
        result = client.generate(
            model="deepseek-coder:6.7b",
            prompt="写一个Python的Hello World程序"
        )
        print("\n生成结果:")
        print(result["response"])
        
    except Exception as e:
        print(f"错误: {e}")
        print("请确保Ollama服务已启动 (运行 'ollama serve')")
