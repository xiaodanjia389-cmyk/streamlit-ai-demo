import os
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings # 如果用通义千问，这里需调整
from langchain.tools import tool
from utils.config_utils import settings
from utils.logger_utils import logger

# --- 任务 2.1：向量存储服务开发 ---
class VectorStoreService:
    def __init__(self):
        self.config = settings['vector_store']
        # 注意：这里需要配置你的 Embedding 模型
        # 如果是通义千问，通常配合 DashScopeEmbeddings 使用
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings['model_config']['api_key'],
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.vector_db = None

    def init_vector_store(self, file_path):
        """加载文档、分块并存入Chroma"""
        logger.info(f"开始加载文档: {file_path}")
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        
        # 分块
        text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
        docs = text_splitter.split_documents(documents)
        
        # 存入 Chroma
        self.vector_db = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=self.config['persist_directory']
        )
        logger.info("向量数据库初始化完成")

    def search(self, query):
        """检索接口"""
        if not self.vector_db:
            return "数据库未初始化"
        results = self.vector_db.similarity_search(query, k=2)
        return "\n".join([doc.page_content for doc in results])

# 实例化服务
service = VectorStoreService()

# --- 任务 2.2：RAG总结工具封装 ---
@tool
def product_knowledge_search(query: str) -> str:
    """
    当用户询问关于扫地机器人的产品规格、故障排查、使用说明或售后政策时，调用此工具。
    输入应该是用户的核心问题。
    """
    logger.info(f"Agent 调用了检索工具，查询词: {query}")
    return service.search(query)

if __name__ == "__main__":
    # 测试代码：先初始化库，再模拟调用工具
    test_file = os.path.join(os.getcwd(), "data", "robot_faq.txt")
    service.init_vector_store(test_file)
    print(f"检索测试结果: {product_knowledge_search('亮红灯怎么办')}")