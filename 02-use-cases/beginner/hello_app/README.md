# 餐厅点餐 Agent (`hello_app`)

本项目展示了一个高级 Agent，其设计目标是成为一个友好且高效的餐厅点餐助手。它展示了 Agent 开发套件（ADK）的几个核心能力。

## 核心功能

该 Agent 的主要目标是帮助用户从预定义的菜单中点餐。它可以：

-   **接收订单**: 理解用户的请求（例如，“我想要一些辣的菜”）并将其与菜单项进行匹配。
-   **添加到订单**: 使用 `add_to_order` 工具将具体的菜品添加到用户的购物车中。
-   **汇总订单**: 使用 `summarize_order` 工具在结账前展示最终的菜品列表。
-   **处理菜单外请求**: 当用户想点的菜不在菜单上时，Agent会利用`web_search`工具进行网络搜索，并与用户确认是否作为特殊菜品下单。

## 特殊能力与高级特性

该 Agent 不仅仅局限于基础对话，还展示了几个强大的高级特性：

### 1. 异步工具与并行调用

为了提升响应效率，本项目中的工具（如 `add_to_order`）被定义为异步函数（`async def`）。更重要的是，在 Agent 的核心指令（Instruction）中，明确鼓励模型在需要时**并行调用**这些工具。

> **提示词指令**: `You can using parallel invocations to add multiple dishes to the order.`

这意味着当用户一次性说出“我要一个宫保鸡丁和一份饺子”时，Agent 可以同时发起两个 `add_to_order` 的工具调用，从而显著加快处理速度。

### 2. 高级上下文管理与压缩

为了在长对话中保持高效并节省成本，本项目运用了两种高级上下文管理技术：

-   **事件压缩 (`EventsCompactionConfig`)**: 这是本项目的亮点之一。通过配置 `EventsCompactionConfig`，Agent 可以自动将多轮对话历史进行“压缩”，生成一个简洁的摘要。这避免了在每次请求时都传递完整的、冗长的对话历史，极大地节省了 Token 数量。
    > **代码注释**: `events_compaction_config 用于配置事件压缩，以在长对话中节省上下文。`
-   **上下文过滤器 (`ContextFilterPlugin`)**: 作为补充，`ContextFilterPlugin` 插件被用来精确控制保留最近的几轮对话（例如，保留最近8轮），确保核心上下文不丢失。

### 3. 使用 `ToolContext` 进行状态管理

Agent 能够在多轮对话中持续维护用户的订单状态。它通过使用 `tool_context.state` 字典来实现这一点，这是一个在工具调用之间传递和共享的持久化状态。

-   `add_to_order` 工具会将新菜品添加到一个位于 `tool_context.state["order"]` 内的列表中。
-   `summarize_order` 工具会从这个共享状态中读取数据，以提供完整的订单摘要。

### 4. 自定义插件 (`CountInvocationPlugin`)

该项目包含一个自定义插件 `CountInvocationPlugin`，它会挂载到 Agent 的生命周期中，用于实时统计 Agent 的运行次数和底层大语言模型（LLM）的调用次数。

这演示了如何利用插件机制对 Agent 的内部行为进行监控、记录日志或注入自定义逻辑，为 Agent 的可观测性提供了强大的支持。