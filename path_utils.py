import os

def get_project_root():
    """自动获取项目根目录的绝对路径 [cite: 159]"""
    # 获取当前文件 (path_utils.py) 的绝对路径
    current_path = os.path.abspath(__file__)
    # 连续向上退两级：从 utils/ 目录退回到 Agent_Project/ 根目录
    project_root = os.path.dirname(os.path.dirname(current_path))
    return project_root

# 定义全局变量 PROJECT_ROOT，方便整个项目统一调用 [cite: 159]
PROJECT_ROOT = get_project_root()

if __name__ == "__main__":
    print(f"项目根目录确认成功: {PROJECT_ROOT}")