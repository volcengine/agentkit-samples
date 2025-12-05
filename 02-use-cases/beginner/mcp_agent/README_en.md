# MCP Agent Demo

## Introduction
Integrate Volcano MCP Server as a tool into Agent to implement Torch Object Storage (TOS) management operations.

## Project Description
This example demonstrates the integration of VeADK with MCP tools:
- **MCP Tool Integration**: Use `MCPToolset` to connect to [Volcano MCP Server](https://www.volcengine.com/mcp-marketplace) service
- **Object Storage Operations**: Agent can execute various TOS object storage management operations through the MCP protocol
- **Tool Invocation**: Agent automatically identifies user intent and invokes corresponding MCP tools to complete tasks

Code Structure:
- Use environment variable `TOOL_TOS_URL` to configure MCP service address
- `MCPToolset` manages connections and tool invocations with MCP service
- Agent has professional object storage management capabilities

## Prerequisites
1. **Enable Volcano Ark Model Service**: Visit [Ark console](https://exp.volcengine.com/ark?mode=chat)
2. **Prepare model_api_key**: Obtain **API Key** from the console
3. **Deploy MCP Service**: Install [TOS MCP](https://www.volcengine.com/mcp-marketplace/detail?name=TOS%20MCP) on Volcano MCP Server

## How to Run
### 1. Install veadk and agentkit python sdk, configure environment variables

```bash
uv pip install veadk-python
uv pip install agentkit-sdk-python
```

Set your model information and TOS MCP in `config.yaml`:
```yaml
model:
  agent:
    name: doubao-seed-1-6-251015
    api_key: XXXX

tool:
  tos:
    url: XXX
```

### 2. Run local client
```bash
cd mcp_agent
python agent.py
```

### 3. Run veadk web client and access via browser at http://127.0.0.1:8000
```bash
cd ..
veadk web
```

### 4. Deploy to vefaas
> **Security Warning: Do not disable key authentication in production environments. Ensure `VEFAAS_ENABLE_KEY_AUTH` remains `true` (or unset, defaulting to enabled), and properly configure access keys and roles. Only temporarily disable authentication in local controlled debugging environments, and make sure to include warnings.**

```bash
cd mcp_agent
# Run this step directly
export VEFAAS_ENABLE_KEY_AUTH=false
# Replace YOUR_AK with your own access key
export VOLCENGINE_ACCESS_KEY=YOUR_AK
# Replace YOUR_SK with your own secret key
export VOLCENGINE_SECRET_KEY=YOUR_SK
# Deploy application to cloud
veadk deploy --vefaas-app-name=mcp-agent --use-adk-web --veapig-instance-name=<your veapig instance name> --iam-role "trn:iam::<your account id>:role/<your iam role name>"
```

### 5. Deploy to AgentKit and test with client.py

```bash
cd mcp_agent
# Uncomment the following line in agent.py to run the agentkit app server
# agent_server_app.run(host="0.0.0.0", port=8000)
agentkit config
agentkit launch
```

## Example Prompts

- Query bucket list:
> What buckets are available under the current account?

- Query object list:
> What files are in bucket-prod?

- Read text file content:
> Read the content of config.txt in the files directory of bucket-prod