import hashlib
import os
from utils.logger_utils import logger

def calculate_md5(file_path):
    """任务 1.4：计算文件MD5，用于知识库去重"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_all_files(directory):
    """任务 1.4：扫描文件夹下所有支持的文档"""
    # 增加格式过滤，目前支持 txt, md, pdf
    supported_extensions = ('.txt', '.md', '.pdf')
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_extensions):
                file_list.append(os.path.join(root, file))
    
    logger.info(f"扫描完成，共发现 {len(file_list)} 个有效文档")
    return file_list

if __name__ == "__main__":
    # 测试一下扫描 data 文件夹
    from utils.path_utils import PROJECT_ROOT
    data_path = os.path.join(PROJECT_ROOT, "data")
    files = get_all_files(data_path)
    print(f"待处理文件列表: {files}")