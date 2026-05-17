# Project Overview
为时12周的Agent学习项目。
# Features
# Architecture
# Tech Stack
Python + FastApi + Streamlit UI + pickle
## Tool Calling
### What Is Tool Calling
Tool Calling 即是由模型来决定是否调用工具并且给出调用工具的具体指令，由应用侧进行具体的执行并且给模型返回执行的结果，模型结合返回的结果给出最终回答。
### 模型负责什么。
模型需要知道可以使用的工具，并且根据用户的提供具体分析是否需要使用工具，是用什么工具，具体怎么用，设计期望的返回格式。然后根据应用端执行的结果进行最终回答。
### 后端负责什么。
后端负责按照模型给出的工具执行指令进行具体的执行并且按照期望格式给模型返回执行的结果。
### 工具 Schema 是什么
定义可用工具列表以及它们是如何接收和返回数据的。
### 为什么工具执行不能交给模型。
因为模型受权限限制，不能直接操作用户的应用。
### 它和 RAG 的区别是什么。
RAG是利用已有的资料文件进行查询并且返回和提问相关的片段，而Tool Calling则是选取可用工具并且设计工具指令，指导应用端进行具体执行，并且获取执行结果，而不是搜索操作。
### 它和 Agent 的关系是什么。
它是Agent可选的操作之一，与RAG并列。

# Setup
# Environment Variables
# How to Build Index
# How to Run API
# How to Run UI
# API Example
# Demo Screenshots
# Current Limitations
# Current Goals
## Week 5
### Expected Reaction
POST /tool/chat
- request: question, top_k
- response: answer, tool_calls, sources
    - Return sources only when called search_knowledge_base
    - Tool_calls includes which tools are called, what parameters are sent, the summary of what are returned from tools

### 
# Next Steps