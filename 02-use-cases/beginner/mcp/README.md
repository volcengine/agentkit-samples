# MCP Agent Demo

## 简介
将火山 MCP Server 以工具形式集成到 Agent，实现对象存储（TOS）的管理操作

## 项目说明
本示例演示了 VeADK 与 MCP 工具的集成：
- **MCP 工具集成**：使用 `MCPToolset` 连接[火山 MCP Server](https://www.volcengine.com/mcp-marketplace) 服务
- **对象存储操作**：Agent 可以通过 MCP 协议执行 TOS 对象存储的各种管理操作
- **工具调用**：Agent 自动识别用户意图，调用相应的 MCP 工具完成任务

代码结构：
- 使用环境变量 `TOOL_TOS_URL` 配置 MCP 服务地址
- `MCPToolset` 管理与 MCP 服务的连接和工具调用
- Agent 具备专业的对象存储管理能力

## 前置依赖
1. **开通火山方舟模型服务**：前往 [Ark console](https://exp.volcengine.com/ark?mode=chat)
2. **准备 model_api_key**：在控制台获取 **API Key**
3. **部署 MCP 服务**：在火山 MCP Server 安装 [TOS MCP](https://www.volcengine.com/mcp-marketplace/detail?name=TOS%20MCP)

## 运行方法
### 1. 配置环境变量
在 `config.yaml` 中设置你的模型信息以及 TOS MCP：
```yaml
model:
  agent:
    name: doubao-seed-1-6-251015
    api_key: XXXX

tool:
  tos:
    url: XXX
```

### 2. 运行本地客户端
```bash
python agent.py
```

## 示例 Prompt

- 查询存储桶列表：
> 当前账号下有哪些存储桶

- 查询对象列表：
> bucket-prod 里面有哪些文件？

- 读取文本文件内容：
> 读取 bucket-prod 中 files 目录下 config.txt 的内容

