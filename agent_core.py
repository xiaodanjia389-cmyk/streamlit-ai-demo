from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain import hub
from utils.config_utils import settings
from utils.business_tools import tools
from utils.middleware_utils import (
    model_call_monitor_middleware,
    dynamic_prompt_middleware
)

class ReActAgent:
    def __init__(self):
        # 1. 实例化原始模型
        raw_model = ChatOpenAI(
            model=settings['model_config']['model_name'],
            openai_api_key=settings['model_config']['api_key'],
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
            temperature=0
        )
        
        # 2. 核心修正：创建一个包装后的 invoke 函数
        # 我们不修改 raw_model，而是定义一个具备中间件功能的函数
        monitored_invoke = dynamic_prompt_middleware(
            model_call_monitor_middleware(raw_model.invoke)
        )
        
        # 3. 将这个函数重新绑定（绕过 Pydantic 检查）
        # 我们直接把 raw_model 的 invoke 引用指向我们的包装函数
        # 如果直接赋值不行，我们用这个特殊技巧：
        object.__setattr__(raw_model, 'invoke', monitored_invoke)
        self.chat_model = raw_model

        # 4. 剩余逻辑保持不变
        self.prompt = hub.pull("hwchase17/openai-tools-agent")
        agent = create_tool_calling_agent(self.chat_model, tools, self.prompt)
        
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def execute_stream(self, query: str):
        # 执行流式输出
        for chunk in self.agent_executor.stream({"input": query}):
            if "output" in chunk:
                yield chunk["output"]

if __name__ == "__main__":
    print("--- [系统启动] 正在进行最终适配测试 ---")
    agent = ReActAgent()
    for response in agent.execute_stream("你好"):
        print(response, end="", flush=True)