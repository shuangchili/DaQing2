# sgcc_project/module_5/module_5_1/llm_service.py
import requests
import json
import re
# 使用相对导入
from .config import Config
from .prompts import SYSTEM_PROMPTS, get_user_prompt

def call_ai_evaluation(feature_name, file_content):
    """
    组装提示词并调用阿里云百炼 API
    """
    system_prompt = SYSTEM_PROMPTS.get(feature_name, "你是一个有用的助手。")
    user_prompt = get_user_prompt(feature_name, file_content)
    
    headers = {
        # 修改这里：使用阿里云的配置
        "Authorization": f"Bearer {Config.ALIYUN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": Config.MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        # qwen-plus 通常支持 json_object 模式，但也取决于具体版本
        # 为了稳妥，我们可以保留这个参数，如果报错再去掉
        "response_format": {"type": "json_object"},
        "temperature": 0.1
    }

    try:
        response = requests.post(Config.BASE_URL, headers=headers, json=payload)
        
        # 增加错误处理打印，方便调试
        if response.status_code != 200:
            return {"error": f"API请求失败 (HTTP {response.status_code})", "details": response.text}

        response_data = response.json()
        
        if "choices" in response_data and len(response_data["choices"]) > 0:
            content = response_data['choices'][0]['message']['content']
            
            # 清洗 Markdown 标记 (例如 ```json ... ```)
            content = re.sub(r'```json\s*|\s*```', '', content)
            
            try:
                # 尝试解析 JSON
                return json.loads(content)
            except json.JSONDecodeError:
                # 如果解析失败，可能是模型返回了非标准JSON，返回原始内容以供检查
                return {"error": "模型返回内容格式错误，无法解析为JSON", "raw_content": content}
        
        elif "code" in response_data:
            # 阿里云特定的错误返回结构
            return {"error": f"阿里云API错误: {response_data.get('message')}", "code": response_data.get('code')}
            
        else:
            return {"error": "未知API响应结构", "details": response_data}
            
    except Exception as e:
        return {"error": "请求异常", "details": str(e)}