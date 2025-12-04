# Multi Agents

## 简介
使用 VeADK 构建一个由多个专业 Agent 组成的协作系统

## 项目说明
本示例演示了一个典型的多智能体协作场景：
- **层级架构**：主 Agent 负责任务分发，子 Agent 负责具体执行
- **专业分工**：每个 Agent 专注于特定领域（如存储管理、数据查询等）
- **工具集成**：集成火山引擎服务作为工具能力
- **协作流程**：Agent 之间通过消息传递和结果共享完成复杂任务

多智能体结构：
<img src="./doc/architecture.jpeg" alt="assistant_agent" width="100%">

## 前置依赖
1. **开通火山方舟模型服务**：前往 [Ark console](https://exp.volcengine.com/ark?mode=chat)
2. **准备 model_api_key**：在控制台获取 **API Key**。
3. **获取 AK、SK**：参考 [用户指南](https://www.volcengine.com/docs/6291/65568?lang=zh)获取火山引擎访问密钥

## 运行方法
### 1. 配置环境变量
在 `config.yaml` 中设置你的模型信息及 AK、SK：
```yaml
model:
  agent:
    name: doubao-seed-1-6-251015
    api_key: XXXX

volcengine:
  access_key: XXXX
  secret_key: XXXX
```

### 2. 运行智能体

**方式一：使用 Web 界面调试**
```bash
cd 02-use-cases/beginner
veadk web
# 在浏览器打开 http://127.0.0.1:8000
# 在左上角选择 multi_agents 这个 agent，即可开始调试
```

**方式二：使用命令行**
```bash
cd 02-use-cases/beginner
python multi_agents/main.py
```

## 示例 Prompt
- 简单打招呼：
> 你好，你能提供什么帮助？

- 商品咨询与推荐
> 我想买一台火山引擎虚拟机，用来做图像处理，可以帮我介绍一下哪个规格更适合我吗？

- 订单查询与问题处理
> 我的订单 12345 什么时候发货？已经等了 3 天了

