import os
from utils.path_utils import PROJECT_ROOT
from utils.logger_utils import logger

class PromptLoader:
    """
    任务 1.5：提示词加载工具
    统一管理系统、RAG、报告生成等各类提示词模版
    """
    def __init__(self):
        # 提示词文件夹路径
        self.prompt_dir = os.path.join(PROJECT_ROOT, "config", "prompts")

    def get_prompt(self, filename):
        """根据文件名读取提示词内容"""
        file_path = os.path.join(self.prompt_dir, filename)
        try:
            if not os.path.exists(file_path):
                logger.error(f"未找到提示词文件: {filename}")
                return ""
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                logger.info(f"成功加载提示词: {filename}")
                return content
        except Exception as e:
            logger.error(f"加载提示词文件 {filename} 失败: {str(e)}")
            return ""

# 实例化
prompt_loader = PromptLoader()

if __name__ == "__main__":
    # 测试动态切换
    print("--- 提示词加载工具验证 ---")
    sys_p = prompt_loader.get_prompt("system_prompt.txt")
    rag_p = prompt_loader.get_prompt("rag_prompt.txt")
    
    print(f"系统提示词预览: {sys_p[:20]}...")
    print(f"RAG提示词预览: {rag_p[:20]}...")