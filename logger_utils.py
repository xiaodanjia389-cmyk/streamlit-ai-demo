import logging
import os
from datetime import datetime
from utils.path_utils import PROJECT_ROOT

def get_logger(name="Agent_System"):
    # 1. 创建日志文件夹
    log_dir = os.path.join(PROJECT_ROOT, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 2. 生成以日期命名的文件名
    log_filename = f"{datetime.now().strftime('%Y-%m-%d')}.log"
    log_path = os.path.join(log_dir, log_filename)
    
    # 3. 初始化 logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 避免重复添加 Handler
    if not logger.handlers:
        # 格式设置：时间 - 名称 - 级别 - 内容
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # 文件输出
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

# 创建全局 logger 实例
logger = get_logger()

if __name__ == "__main__":
    logger.info("日志系统初始化成功！")