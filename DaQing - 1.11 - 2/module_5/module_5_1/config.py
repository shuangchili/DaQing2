# sgcc_project/module_5/module_5_1/config.py
import os

class Config:
    # ================= 阿里云百炼配置 =================
    # 您的 API Key
    ALIYUN_API_KEY = "sk-d3c411507dc345adba1c76ae889aee40"
    
    # 阿里云百炼 OpenAI 兼容模式接口地址
    BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    
    # 指定模型版本
    MODEL_NAME = "qwen-plus-2025-07-28"
    # =================================================
    
    # 文件上传允许的扩展名
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}