import os
import json
import uuid
from flask import render_template, request, current_app, flash
# 从当前包导入 blueprint
from . import eval_bp
# 导入同目录下的服务模块
from .config import Config
from .file_handler import extract_text_from_file 
from .llm_service import call_ai_evaluation

# 1. 对应 app.py 中 redirect(url_for('eval_5_1.entry_point', ...)) 的路由
@eval_bp.route('/entry/<level1>/<level2>/<feature_name>')
def entry_point(level1, level2, feature_name):
    return render_template('feature_eval.html', 
                           l1=level1, 
                           l2=level2, 
                           feature_name=feature_name,
                           result=None)

# 2. 处理文件上传和评测的路由
@eval_bp.route('/process/<level1>/<level2>/<feature_name>', methods=['POST'])
def process(level1, level2, feature_name):
    # 使用 current_app 获取全局配置的上传路径
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    
    if 'file' not in request.files:
        return render_template('feature_eval.html', l1=level1, l2=level2, feature_name=feature_name, error="未上传文件")
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template('feature_eval.html', l1=level1, l2=level2, feature_name=feature_name, error="文件名为空")

    # 获取文件后缀
    _, file_ext = os.path.splitext(file.filename)
    file_ext = file_ext.lower()

    # 检查后缀是否允许
    if file_ext.lstrip('.') in Config.ALLOWED_EXTENSIONS:
        # 使用 UUID 重命名文件，避免中文乱码问题
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        filepath = os.path.join(upload_folder, unique_filename)
        
        try:
            file.save(filepath)
            
            # 提取文本
            file_content = extract_text_from_file(filepath)
            print(f"DEBUG: 文件名={file.filename}, 提取字数={len(file_content)}")

            # 拦截空内容
            if not file_content or len(file_content.strip()) < 10:
                try: os.remove(filepath) 
                except: pass
                return render_template('feature_eval.html', 
                                       l1=level1, 
                                       l2=level2, 
                                       feature_name=feature_name, 
                                       error=f"读取失败：提取到的有效文字过少（{len(file_content)}字）。")

            # 调用AI服务
            ai_result = call_ai_evaluation(feature_name, file_content)
            
            # 格式化结果为字符串以便前端显示
            if isinstance(ai_result, (dict, list)):
                ai_result_str = json.dumps(ai_result, ensure_ascii=False, indent=4)
            else:
                ai_result_str = str(ai_result)

            # 可选：处理完删除文件
            # os.remove(filepath)

            return render_template('feature_eval.html', 
                                   l1=level1, 
                                   l2=level2, 
                                   feature_name=feature_name, 
                                   result=ai_result_str)
                                   
        except Exception as e:
            return render_template('feature_eval.html', l1=level1, l2=level2, feature_name=feature_name, error=f"系统处理异常: {str(e)}")
    
    return render_template('feature_eval.html', l1=level1, l2=level2, feature_name=feature_name, error="不支持的文件格式")