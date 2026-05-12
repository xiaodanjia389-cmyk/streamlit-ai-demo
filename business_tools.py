import random
from langchain.tools import tool
from utils.logger_utils import logger
from utils.vector_service import VectorStoreService
# 导入任务 3.1 开发的中间件
from utils.middleware_utils import tool_monitor_middleware

# 实例化向量服务（自动加载 ./chroma_db）
vector_service = VectorStoreService()

@tool
@tool_monitor_middleware
def get_weather(city: str) -> str:
    """
    查询指定城市的实时天气情况。
    当用户询问某个城市的天气、气温或是否需要带伞时，请调用此工具。
    参数说明：city 为城市名称（如：北京、上海）。
    """
    logger.info(f"执行业务工具 - 天气查询: {city}")
    
    # 模拟数据
    weather_list = ["晴", "多云", "阴", "小雨"]
    temp = random.randint(10, 30)
    weather = random.choice(weather_list)
    
    return f"{city}当前天气为{weather}，气温{temp}℃。"

@tool
@tool_monitor_middleware
def get_user_info() -> str:
    """
    获取当前用户的个人信息和产品状态。
    当用户询问“我是谁”、“我的保修期还有多久”或“我买的是哪款机器”时，调用此工具。
    """
    logger.info("执行业务工具 - 获取用户信息")
    
    # 模拟从数据库读取用户信息
    user_data = {
        "user_name": "张三",
        "product_model": "扫地宝 X20 Pro",
        "warranty_days": 156,
        "last_cleaning": "2026-04-23"
    }
    
    return (f"用户信息：{user_data['user_name']}\n"
            f"购买机型：{user_data['product_model']}\n"
            f"剩余保修：{user_data['warranty_days']}天\n"
            f"上次清扫：{user_data['last_cleaning']}")

@tool
@tool_monitor_middleware
def knowledge_search(query: str) -> str:
    """
    当用户询问扫地机器人的产品参数、故障排查（如亮红灯）、保养建议或使用说明时，调用此工具。
    输入应该是具体的查询词。
    """
    logger.info(f"执行业务工具 - 知识库检索: {query}")
    # 调用任务 2.1 开发的标准化检索接口
    return vector_service.query(query)

# 定义工具列表，方便后续 Agent 调用
tools = [get_weather, get_user_info, knowledge_search]

if __name__ == "__main__":
    # 验证工具是否能独立运行并触发监控日志
    print("--- 业务工具集成测试 (含中间件监控) ---")
    print(f"1. 天气工具测试: {get_weather.run('北京')}")
    print("-" * 30)
    print(f"2. 用户信息测试: {get_user_info.run({})}")
    print("-" * 30)
    print(f"3. 知识库检索测试: {knowledge_search.run('亮红灯')}")