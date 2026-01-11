import os
from flask import Flask, render_template, redirect, url_for
from registry import menu_registry  # 导入注册中心

# ==========================================
# 模块导入区
# 只要导入了包，它们内部的 __init__.py 就会运行，
# 从而自动执行 menu_registry.register()
# ==========================================
import module_5.module_5_1  # 导入 5-1
# import module_5.module_5_2  #以此类推，未来直接解开注释即可接入新模块

app = Flask(__name__)

# 注册蓝图 (这一步也可以优化进 registry，但为了显式控制建议保留)
app.register_blueprint(module_5.module_5_1.eval_bp)
# app.register_blueprint(module_5.module_5_2.bp_5_2)

# 全局变量注入：直接从 registry 获取最新的 DATA
@app.context_processor
def inject_global_vars():
    return dict(DATA=menu_registry.menu_data)

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# 二级页面路由 (通用逻辑，无需修改)
@app.route('/module/<level1_name>')
def level2_view(level1_name):
    data = menu_registry.menu_data # 获取动态数据
    if level1_name not in data:
        return "Module not found", 404
    modules = list(data[level1_name].keys())
    return render_template('level2.html', active_l1=level1_name, modules=modules)

# 三级页面路由
@app.route('/module/<level1_name>/<level2_name>')
def level3_view(level1_name, level2_name):
    data = menu_registry.menu_data
    if level1_name not in data or level2_name not in data[level1_name]:
        return "Module not found", 404
    modules = data[level1_name][level2_name]
    return render_template('level3.html', active_l1=level1_name, active_l2=level2_name, modules=modules)

# 功能执行路由分发器
@app.route('/feature/<level1>/<level2>/<feature_name>')
def feature_interface(level1, level2, feature_name):
    # 这里需要一个机制来判断 feature 属于哪个蓝图
    # 简单的方式是：如果属于评测，转发给评测蓝图
    # 更好的方式是：在 registry 里同时注册路由处理函数（略复杂，暂维持现状）
    
    # 示例：如果是 5-1 的功能，跳转
    if level1 == "质量评测" and level2 == "智能自动评估":
         return redirect(url_for('eval_5_1.entry_point', level1=level1, level2=level2, feature_name=feature_name))

    return render_template('feature.html', active_l1=level1, active_l2=level2, feature_name=feature_name)

if __name__ == '__main__':
    app.run(debug=True, port=5000)