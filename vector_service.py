import os
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
# 引入通义千问原生向量化工具
from langchain_community.embeddings import DashScopeEmbeddings
from utils.config_utils import settings
from utils.logger_utils import logger

class VectorStoreService:
    """任务 2.1：基于 Chroma 的向量存储服务 (通义千问版)"""
    
    def __init__(self):
        # 从 settings.yaml 加载配置
        self.config = settings['vector_store']
        
        # 使用通义千问原生向量模型
        self.embeddings = DashScopeEmbeddings(
            model="text-embedding-v2", 
            dashscope_api_key=settings['model_config']['api_key']
        )
        self.vector_db = None

    def load_and_index(self, file_path):
        """加载、切分并向量化"""
        logger.info(f"正在向量化处理文档: {file_path}")
        
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        
        # 任务 2.1 要求：分块处理
        text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)
        
        # 存入 Chroma 本地数据库
        self.vector_db = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=self.config['persist_directory']
        )
        logger.info(f"向量化存储完成！数据库位于: {self.config['persist_directory']}")

    def query(self, text):
        """标准化检索接口"""
        if not self.vector_db:
            self.vector_db = Chroma(
                persist_directory=self.config['persist_directory'],
                embedding_function=self.embeddings
            )
        docs = self.vector_db.similarity_search(text, k=2)
        return "\n".join([doc.page_content for doc in docs])

if __name__ == "__main__":
    print("VectorStoreService (DashScope) 准备就绪")