import functools
import time
from utils.logger_utils import logger
# --- 关键：添加以下这一行导入 ---
from langchain_core.messages import SystemMessage, HumanMessage 

def tool_monitor_middleware(func):
    # ... 后面的代码保持不变 ...
    import functools
import time
from utils.logger_utils import logger

def tool_monitor_middleware(func):
    """
    任务 3.1：工具调用监控中间件
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tool_name = func.__name__
        start_time = time.time()
        logger.info(f"--- [工具启动] 名称: {tool_name} ---")
        try:
            result = func(*args, **kwargs)
            duration = round(time.time() - start_time, 4)
            logger.info(f"--- [执行成功] 耗时: {duration}s ---")
            return result
        except Exception as e:
            logger.error(f"--- [执行异常] {tool_name}: {str(e)} ---")
            raise e
    return wrapper

def model_call_monitor_middleware(func):
    """
    任务 3.2：模型调用日志中间件
    在模型每次调用前记录消息数量与内容，监控思考过程。
    """
    @functools.wraps(func)
    def wrapper(messages, *args, **kwargs):
        # 核心逻辑必须缩进！
        msg_count = len(messages)
        logger.info(f"--- [模型决策启动] ---")
        logger.info(f"--- [上下文消息数] {msg_count} 条 ---")
        
        if msg_count > 0:
            last_msg = messages[-1]
            content = getattr(last_msg, 'content', str(last_msg))
            logger.info(f"--- [最新输入内容] {content[:50]}... ---")
            
        result = func(messages, *args, **kwargs)
        logger.info(f"--- [模型响应完成] ---")
        return result
        
    return wrapper
    from langchain_core.messages import SystemMessage

def dynamic_prompt_middleware(func):
    """
    任务 3.4：动态提示词切换中间件
    根据用户输入的关键词，动态调整系统提示词（System Prompt）。
    """
    @functools.wraps(func)
    def wrapper(messages, *args, **kwargs):
        # 1. 提取用户最新的提问内容
        user_input = ""
        if len(messages) > 0:
            user_input = getattr(messages[-1], 'content', "").lower()
        
        # 2. 场景识别逻辑
        report_keywords = ["报告", "生成文档", "清扫总结", "汇总"]
        is_report_scene = any(word in user_input for word in report_keywords)
        
        # 3. 动态切换提示词
        if is_report_scene:
            logger.info("--- [提示词切换] 检测到报告生成需求，切换至『专业报告模式』 ---")
            report_prompt = (
                "你现在是一名专业的机器人数据分析师。请根据工具返回的数据，"
                "生成一份排版精美、格式正式的使用报告，包含清扫结论、健康建议和维护提醒。"
            )
            # 修改系统提示词（假设第一条是 SystemMessage）
            if len(messages) > 0 and isinstance(messages[0], SystemMessage):
                messages[0].content = report_prompt
        else:
            logger.info("--- [提示词模式] 保持『基础客服模式』 ---")
            
        return func(messages, *args, **kwargs)
        
    return wrapper