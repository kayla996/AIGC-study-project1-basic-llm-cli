# Tool Calling 和普通 Prompt 有什么区别？
普通 Prompt 中，模型主要根据 messages 直接生成自然语言回答。Tool Calling 中，应用会把可用工具的名称、描述和参数 schema 一起传给模型，模型可以选择直接回答，也可以返回结构化的 tool_calls。应用侧接收到 tool_calls 后执行对应工具，再把 tool 结果作为新消息传回模型，由模型生成最终回答。因此 Tool Calling 的关键区别是：模型不仅能“回答”，还能“提出工具调用请求”，但工具执行仍由应用侧完成。
另一方面，tool calling可能会至少比普通的prompt多调用一轮。普通prompt调用顺序为：
“system...系统/用户prompt”
“user...用户问题/请求”
“assistant...响应问题”

tool calling：
“system...系统/用户prompt”
“user...用户问题/请求”
“assistant...响应问题直接结束/工具调用指令”
“tool...对应工具调用结果”
“assistant...响应问题结束/工具调用指令”

# Tool Calling 和 RAG 有什么关系？
RAG 是一种“检索增强生成”的能力，它本身不等于 Tool Calling。传统 RAG 是应用侧固定先检索，再把 chunks 拼进 prompt 给模型。Tool Calling 中可以把 RAG 检索封装成 search_knowledge_base 工具，让模型在需要知识库时主动请求检索。因此二者关系是：RAG 可以作为 Tool Calling 的一个工具，但也可以作为固定前置流程独立存在。两者的关键区别在于控制权：传统 RAG 由应用侧决定检索，Tool Calling 方式下模型可以参与决定是否调用检索工具。

# 为什么工具执行必须在应用侧？
工具必须在应用侧执行，因为 LLM 只能生成结构化的工具调用请求，不能真正运行本地函数、访问数据库或调用外部 API。实际执行函数、检查参数、控制权限、处理异常、记录日志，都必须由后端应用完成。这样也能避免模型绕过安全边界直接操作系统资源。

# 模型什么时候可能不调用工具？
1. 问题非常简单，模型认为自己可以直接回答。
2. 工具描述不够清楚，模型不知道该用哪个工具。
3. 用户问题和工具能力不匹配。
4. system prompt 没有要求模型必要时使用工具。
5. tool_choice 设置为 "none"，强制不允许调用工具。
6. 模型判断调用工具成本不必要。

# 如果工具调用参数错了怎么办？
如果工具调用参数错了，应用侧不应该直接执行，而应该先解析和校验参数。例如使用 CalculatorArgs 或 KnowledgeBaseSearchArgs 做 model_validate。如果字段缺失、类型错误、top_k 越界或 query 为空，ToolExecutor 应该捕获 ValidationError，返回 success=False 和 error 信息。随后可以把这个错误结果返回给模型，让模型解释失败原因，或者在多轮 Agent 中尝试重新生成正确参数。

# 为什么要限制工具调用轮数？
第一，控制成本。每多调用一轮模型和工具，都会增加 token、API 调用和时间成本。
第二，避免不可控行为。尤其工具多了以后，模型可能反复检索、反复计算、反复调用无关工具。

# Tool Calling 和 Agent 的关系是什么？
Tool Calling 是 Agent 的基础能力之一，它让模型具备“请求调用外部工具”的能力。但 Agent 不只是一次工具调用，而是把模型、工具、状态、任务规划、循环执行、错误处理和停止条件组织成一个更完整的自动化流程。简单 Tool Calling 通常是一轮：模型请求工具，应用执行工具，模型回答；Agent 则可能是多轮、多工具、多步骤的决策和执行过程。