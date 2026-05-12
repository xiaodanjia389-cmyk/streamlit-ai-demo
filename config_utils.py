import yaml
import os
from utils.path_utils import PROJECT_ROOT

def load_config():
    """实现YAML配置文件的加载与管理 """
    # 拼接配置文件的绝对路径
    config_path = os.path.join(PROJECT_ROOT, "config", "settings.yaml")
    
    # 如果文件不存在，给出一个友好的提示
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件未找到: {config_path}，请先创建它。")
        
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

# 全局配置实例，方便其他模块直接调用
settings = load_config()

if __name__ == "__main__":
    print(f"配置加载成功！当前模型名称: {settings['model_config']['model_name']}")