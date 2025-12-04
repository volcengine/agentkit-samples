import os
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from veadk import Agent, Runner

url = os.getenv("TOOL_TOS_URL")

tos_mcp_runner = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=url,
        timeout=120
    ),
)

root_agent = Agent(
    name="tos_mcp_agent",
    instruction="你是一个对象存储管理专家，精通使用MCP协议进行对象存储的各种操作。",
    tools=[tos_mcp_runner],
)

runner = Runner(agent=root_agent)

async def main(prompt: str) -> str:
    response = await runner.run(messages=prompt)
    return response

if __name__ == "__main__":
    import asyncio

    user_input = "读取 agentkit-skills 桶里的 task_20251203_171710.txt 文件内容"

    response = asyncio.run(main(user_input))
    print(response)