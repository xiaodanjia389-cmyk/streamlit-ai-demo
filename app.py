import streamlit as st
from agent_core import ReActAgent
import time

# --- 1. 页面基本配置 ---
st.set_page_config(
    page_title="iRobot 智能客服中心",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 iRobot 智能客服")
st.caption("基于 Qwen-Max 与 ReAct 架构的下一代扫地机助手")

# --- 2. 初始化 Session State (核心：持久化) ---
# 确保 Agent 实例在页面刷新时不会重置，保持对话连贯
if "agent" not in st.session_state:
    with st.spinner("正在唤醒机器人大脑..."):
        st.session_state.agent = ReActAgent()
        st.session_state.messages = [] # 对话历史存储

# --- 3. 渲染历史对话 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. 用户输入处理 ---
if prompt := st.chat_input("您可以问我：怎么保养机器人？或者帮我生成使用报告"):
    # 展示用户消息并存入历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- 5. Agent 响应渲染 (流式输出) ---
    with st.chat_message("assistant"):
        # 创建一个空容器用于逐字显示
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # 调用我们在任务 4 封装的流式接口
            # 注意：Streamlit 的 st.write_stream 可以直接接受生成器
            def response_generator():
                for chunk in st.session_state.agent.execute_stream(prompt):
                    yield chunk + "" # 确保是字符串

            # 执行流式展示
            full_response = st.write_stream(response_generator())
            
            # 保存回复到历史
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_info = f"抱歉，系统暂时出现了一点小问题：{str(e)}"
            st.error(error_info)
            st.session_state.messages.append({"role": "assistant", "content": error_info})

# --- 6. 侧边栏辅助功能 ---
with st.sidebar:
    st.header("系统状态")
    st.success("Agent 核心：已就绪")
    st.info("当前模式：混合检索 + 工具回调")
    if st.button("清空对话历史"):
        st.session_state.messages = []
        st.rerun()