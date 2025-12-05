import os
from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

# Deploy the agent as AgentkitAgentServerApp into the agentkit platform
from agentkit.apps import AgentkitAgentServerApp

url = os.getenv("TOOL_TOS_URL")

tos_mcp_runner = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=url,
        timeout=120
    ),
)

short_term_memory = ShortTermMemory(backend="local")

agent = Agent(
    name="tos_mcp_agent",
    instruction="你是一个对象存储管理专家，精通使用MCP协议进行对象存储的各种操作。",
    tools=[tos_mcp_runner],
)

runner = Runner(agent=agent, short_term_memory=short_term_memory)

async def main(prompt: str) -> str:
    response = await runner.run(messages=prompt)
    return response

# using veadk web for debugging
root_agent = agent

agent_server_app = AgentkitAgentServerApp(
    agent=agent,
    short_term_memory=short_term_memory,
)

if __name__ == "__main__":
    import asyncio

    user_input = "当前账号下有哪些存储桶"
    response = asyncio.run(main(user_input))
    print(response)

    # Uncomment the following line to run the agentkit app server
    # agent_server_app.run(host="0.0.0.0", port=8000)