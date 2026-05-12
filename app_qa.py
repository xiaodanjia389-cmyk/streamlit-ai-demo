import streamlit as st
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

# ==========================================
# 1. 基础配置：解决 API Key 报错问题 [cite: 247]
# ==========================================
# 请将下面的 sk-xxxx 替换为你真实的通义千问 API 密钥
os.environ["DASHSCOPE_API_KEY"] = "sk-3cfbc55025aa444885c6ab92461218e5"

# 页面基础配置
st.set_page_config(page_title="电商服装智能问答系统", page_icon="🛍️")
st.title("🛍️ 电商服装智能问答系统")
st.caption("基于 RAG 技术，为您提供专业的尺码推荐与洗涤建议")

# ==========================================
# 2. 核心后端逻辑：初始化 RAG 链 
# ==========================================
@st.cache_resource # 使用缓存，避免每次对话刷新页面都重新加载数据库
def init_rag_chain():
    # A. 初始化嵌入模型 [cite: 319]
    embeddings = DashScopeEmbeddings(model="text-embedding-v4")
    
    # B. 加载本地向量数据库 [cite: 319]
    # 注意：persist_directory 必须与你实验二任务2中保存的路径一致
    vector_store = Chroma(
        collection_name="clothing_knowledge",
        embedding_function=embeddings,
        persist_directory="./chroma_db" 
    )
    
    # C. 初始化大模型 
    model = ChatTongyi(model="qwen-max")
    
    # D. 定义提示词模板 
    prompt = ChatPromptTemplate.from_messages([
        ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
        ("user", "用户提问: {input}")
    ])
    
    # E. 构建检索器
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    # F. 文档格式化函数 
    def format_docs(docs: list[Document]):
        if not docs:
            return "无相关参考资料"
        return "\n".join([doc.page_content for doc in docs])
    
    # G. 构建完整的 RAG Chain 
    chain = (
        {"input": RunnablePassthrough(), "context": retriever | format_docs}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain

# 尝试初始化系统
try:
    rag_chain = init_rag_chain()
except Exception as e:
    st.error(f"系统初始化失败，请确保已运行过知识库入库脚本。错误详情: {e}")
    st.stop()

# ==========================================
# 3. Streamlit UI 逻辑：对话管理 [cite: 335, 336]
# ==========================================
# 初始化聊天记录（实现持久化渲染） [cite: 336]
if "messages" not in st.session_state:
    st.session_state.messages = []

# 在界面上渲染历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理用户输入
if prompt_input := st.chat_input("有什么可以帮您的？"):
    # 1. 显示并记录用户消息
    st.session_state.messages.append({"role": "user", "content": prompt_input})
    with st.chat_message("user"):
        st.markdown(prompt_input)

    # 2. 调用 RAG 链生成回复
    with st.chat_message("assistant"):
        with st.spinner("正在检索知识库并生成回答..."):
            try:
                # 执行 RAG 链获取结果 
                response = rag_chain.invoke(prompt_input)
                st.markdown(response)
                # 3. 记录助手消息
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"生成回复时出错，请检查 API 状态。错误信息: {e}")