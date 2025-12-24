# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from google.adk.planners import PlanReActPlanner
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StreamableHTTPConnectionParams,
)
from veadk import Agent
from veadk.knowledgebase.knowledgebase import KnowledgeBase
import os
import sys
from pathlib import Path
import logging
from veadk.memory.long_term_memory import LongTermMemory
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.tools.builtin_tools.web_search import web_search
from agentkit.apps import AgentkitAgentServerApp

# 当前目录
sys.path.append(str(Path(__file__).resolve().parent))
# 上层目录
sys.path.append(str(Path(__file__).resolve().parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app_name = "travel_planner_app"

# 1. 配置短期记忆
short_term_memory = ShortTermMemory(backend="local")

# 2. 配置知识库： Viking 向量数据库
knowledge_collection_name = os.getenv("DATABASE_VIKING_COLLECTION", "")
if knowledge_collection_name != "":
    # 使用用户指定的知识库
    knowledge = KnowledgeBase(backend="viking", index=knowledge_collection_name)
else:
    raise ValueError("DATABASE_VIKING_COLLECTION environment variable is not set")
# 依赖tos桶加载知识库内容
tos_bucket_name = os.getenv("DATABASE_TOS_BUCKET", "")
if tos_bucket_name == "":
    raise ValueError("DATABASE_TOS_BUCKET environment variable is not set")
# 从预构建目录加载知识库
try:
    success = knowledge.add_from_directory(
        str(Path(__file__).resolve().parent) + "/knowledgebase_docs",
        tos_bucket_name=tos_bucket_name,
    )
    if success:
        logger.info("Knowledgebase loaded successfully.")
    else:
        logger.info("Failed to load knowledgebase.")
except Exception as e:
    logger.error(f"Failed to load knowledgebase: {e}")

# 3. 配置长期记忆： Viking 向量数据库
memory_collection_name = os.getenv("DATABASE_VIKINGMEM_COLLECTION", "")
if memory_collection_name != "":
    # 使用用户指定的长期记忆库
    long_term_memory = LongTermMemory(
        backend="viking",
        top_k=3,
        index=memory_collection_name,
    )
else:
    raise ValueError("DATABASE_VIKINGMEM_COLLECTION environment variable is not set")


# 4. 配置 Gaode MCP Server
gaode_mcp_api_key = os.getenv("GAODE_MCP_API_KEY", "")

if gaode_mcp_api_key == "":
    raise ValueError("GAODE_MCP_API_KEY environment variable is not set")

url = "https://mcp.amap.com/mcp?key={}".format(os.getenv("GAODE_MCP_API_KEY"))
amap_tool = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        timeout=30,
        url=url,
        # headers={"Authorization": f"Bearer {apikey}"}
    ),
)

# 5. 配置智能体
travel_planner_prompt = """
    你是一个基于高级规划与反应（Plan-ReAct）架构的智能体，能够动态规划和执行复杂任务，灵活调用工具，并根据环境反馈调整策略。
    你的任务是根据用户的需求，制定详细的旅行计划，推荐景点、美食、住宿，并提供实时的交通和天气信息。

    ## 工具使用规范与优先级
    你拥有以下工具，请按此策略调用：
    1. **知识库 (knowledgebase)**：你的知识库包含了通用旅行安全建议，以及小众景点推荐。处理用户问题时，必须先检索知识库。
    2. **记忆库 (long_term_memory)**：在对话开始时，自动读取用户档案；在对话结束时，如有新偏好，询问用户后存入记忆。
    3. **LBS地理信息服务 (amap_tool)**：**所有**涉及地理位置、路线、距离、实时交通、周边搜索的需求，**必须首先调用此工具**。这是位置信息的权威来源。
    4. **联网搜索 (web_search)**：当需要查询**最新、实时**信息时调用此工具（如近期活动、临时闭馆通知、网红新店、最新攻略）。历史或常识性知识优先使用自身知识。

    ## 工作流程
    1. 检索知识库，获取相关旅行建议和小众景点推荐。
    2. 读取长期记忆，了解用户偏好（如预算、兴趣、过敏等）。
    3. 使用amap_tool搜索规划旅行行程、途径景点、美食推荐、酒店推荐。
    4. 使用web_search搜索步骤3中推荐酒店的以下信息，且**必须返回搜索的酒店预订链接**：
        - 实时价格
        - 用户评分
        - 可用优惠
        - 搜索该酒店的预订链接，如：艺龙旅行网（https://www.elong.com/）、去哪儿网（https://www.qunar.com/）、携程（https://www.ctrip.com/）、飞猪酒店（https://www.fliggy.com/?tab=hotel）
    5. 使用web_search获取实时信息，包括景点闭馆通知、网红新店、近期活动等。
    6. 整合以上信息，整理输出行程规划，注意必须严格按照输出格式规范、选择合适的模板，生成最终回复。
    7. 在对话结束时，询问用户是否保存新的偏好到长期记忆。如果用户同意，保存新的偏好到长期记忆。
    8. 始终遵循核心行为准则，确保输出内容专业、可靠、安全。

    ## 输出格式的严格规范（必须遵守）
    你的回复必须是**纯Markdown格式**，并确保在所有平台渲染美观。根据旅行类型，从以下三个模板中选择其一：

    ### 通用模板选择逻辑
    - 若对话提及“亲子”、“带孩子”、“儿童”等 -> 使用 **【亲子游模板】（output_template/children.md）**。
    - 若提及“海岛”、“沙滩”、“度假”、“放松”等 -> 使用 **【海岛度假模板】(output_template/sea.md)**。
    - 其他或综合需求 -> 使用 **【文化探索模板】(output_template/culture.md)**。

    严格按照所选模板的结构和格式输出，不得遗漏任何部分。

    ## 核心行为准则
    1. **主动全面**：除非用户明确指定，否则规划应涵盖景点、餐饮、交通、住宿、贴士等全要素。
    2. **安全可靠**：所有地理位置信息（如景点、酒店）必须通过高德地图工具amap_tool验证。涉及安全（如天气预警、交通管制）必须明确提醒。
    3. **诚实透明**：如果信息不确定或工具未返回结果，如实告知用户，不要编造。
    4. **记忆与个性**：积极利用记忆工具，记住用户的关键偏好（如预算、喜好、厌恶），使推荐越用越懂。
    5. **沟通要求**： 禁止直接将 工具的结果直接输出给用户，你需要结合用户的问题，对工具的结果进行必要的筛选、格式化处理，在输出给用户时，还需要进行必要的润色，使回复内容更加的清晰、准确、简洁。
"""
agent = Agent(
    name="travel_planner_advanced",
    model_name="deepseek-v3-2-251201",
    instruction=travel_planner_prompt,
    planner=PlanReActPlanner(),
    tools=[amap_tool, web_search],
    long_term_memory=long_term_memory,
    knowledgebase=knowledge,
)

root_agent = agent

agent_server_app = AgentkitAgentServerApp(
    agent=agent,
    short_term_memory=short_term_memory,
)

if __name__ == "__main__":
    logger.info("Starting Travel Planner Agent Server...")
    agent_server_app.run(host="0.0.0.0", port=8000)
