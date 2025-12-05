import sys
from pathlib import Path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from veadk import Agent
from sub_agents.sequential_agent import sequential_service_agent
from prompts import CUSTOMER_SERVICE_AGENT_PROMPT, PRE_PROCESS_AGENT_PROMPT

pre_process_agent = Agent(
    name="pre_process_agent",
    description="分析用户需求，提取关键信息",
    instruction=PRE_PROCESS_AGENT_PROMPT,
)

customer_service_agent = Agent(
    name="customer_service_agent",
    description=("你是一个智能客服，根据用户需求，回答用户问题"),
    instruction=CUSTOMER_SERVICE_AGENT_PROMPT,
    sub_agents=[pre_process_agent, sequential_service_agent]
)

root_agent = customer_service_agent