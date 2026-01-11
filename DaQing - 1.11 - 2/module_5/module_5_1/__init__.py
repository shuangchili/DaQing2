from flask import Blueprint
# 【修改处】改为绝对导入，直接从根目录找 registry
from registry import menu_registry 

# 创建蓝图
eval_bp = Blueprint('eval_5_1', __name__, 
                    template_folder='templates',
                    static_folder='static')

# ==========================================
# 模块自配置区域
# ==========================================
# 定义该模块属于哪个一级分类
LEVEL1_NAME = "质量评测"
# 定义该模块的二级名称
LEVEL2_NAME = "智能自动评估"
# 定义该模块包含的功能点
FEATURES = [
    "评审规则引擎自动检测", 
    "光明大模型内容合理性智能评分", 
    "缺陷分级智能标注与提示", 
    "多模态特征融合一致性校验"
]

# 注册自己到全局菜单
menu_registry.register(LEVEL1_NAME, LEVEL2_NAME, FEATURES)

# 导入路由
from . import routes