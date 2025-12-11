import os
import json
import logging
from pathlib import Path

from dotenv import load_dotenv
# 加载 settings.txt（dotenv 格式）
load_dotenv(dotenv_path=str(Path(__file__).resolve().parent / "settings.txt"), override=False)

from veadk import Agent, Runner
from veadk.a2a.agent_card import get_agent_card
from google.adk.a2a.executor.a2a_agent_executor import A2aAgentExecutor
from agentkit.apps import AgentkitA2aApp

import sys
sys.path.append(str(Path(__file__).resolve().parent))
from tools.catalog_discovery import catalog_discovery
from tools.duckdb_sql_execution import duckdb_sql_execution
from tools.lancedb_hybrid_execution import lancedb_hybrid_execution
from tools.video_generation import generate_video_from_images
from prompts import SYSTEM_PROMPT
# Import memory management
from veadk.memory.short_term_memory import ShortTermMemory
from agentkit.apps import AgentkitAgentServerApp

short_term_memory = ShortTermMemory(backend="local")

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# --- Logging Configuration ---
logger = logging.getLogger(__name__)

tools = [catalog_discovery, duckdb_sql_execution, lancedb_hybrid_execution, generate_video_from_images]

# 定义带记忆的 Agent 类
class MemoryAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, input_text, session_id="default", **kwargs):
        # 从记忆中检索历史对话
        history = self.memory_manager.get_messages(session_id=session_id)
        # 构建包含历史对话的完整指令
        full_instruction = self.instruction
        for role, content in history:
            full_instruction += f"\n{role}: {content}"
        self.instruction = full_instruction
        # 处理当前用户输入
        response = super().run(input_text, **kwargs)
        # 将当前交互保存到记忆
        self.memory_manager.add_message(session_id=session_id, role="user", content=input_text)
        self.memory_manager.add_message(session_id=session_id, role="assistant", content=response)
        return response

# 创建带记忆的 Agent
model_name = os.getenv("AGENT_MODEL_NAME", "doubao-seed-1-6-251015")  # 默认使用更主流的豆包模型
root_agent = MemoryAgent(
    description="LanceDB-based data retrieval agent supporting structured and vector queries.",
    instruction=SYSTEM_PROMPT,
    model_name=model_name,
    tools=tools,
    short_term_memory=short_term_memory,
)

runner = Runner(agent=root_agent)

# a2a_app = AgentkitA2aApp()

# @a2a_app.agent_executor(runner=runner)
# class MyAgentExecutor(A2aAgentExecutor):
#     pass

# # 当直接运行此文件时，启动本地服务
# if __name__ == "__main__":
#     logger.info("🚀 正在启动 A2A Agent 服务...")
#     a2a_app.run(
#         agent_card=get_agent_card(agent=root_agent, url="http://127.0.0.1:8000"),
#         host="0.0.0.0",
#         port=8000,
#     )

agent_server_app = AgentkitAgentServerApp(
    agent=root_agent, short_term_memory=short_term_memory,  
)

if __name__ == "__main__":
    agent_server_app.run(host="0.0.0.0", port=8000)