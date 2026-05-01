# Week 1 - LLM CLI Project

A minimal but structured Python LLM application built in Week 1 of my AI application engineering roadmap.

This project starts as a command-line chatbot and is designed to be extended into a FastAPI service, a RAG system, and more advanced AI workflows in later weeks.

## Overview

The goal of this project is not only to call an LLM API, but also to build a clean and extendable code structure from the beginning.

Current progress includes:

- environment-based configuration
- modular code organization
- OpenAI client wrapper
- chat service layer
- logging system
- multi-turn conversation history support
- API router scaffold prepared for the next phase

## Current Features

- Ask questions from the terminal
- Load configuration from `.env`
- Use a configurable model and system prompt
- Maintain chat history in the service layer
- Structured logging to console and log files
- Clean separation of concerns for future extension

## Project Structure

```text
PROJECT1/
├── app/
│   ├── api/
│   │   ├── chat_router.py
│   │   └── __init__.py
│   ├── chat_service.py
│   ├── config.py
│   ├── llm_client.py
│   ├── logger.py
│   ├── prompts.py
│   └── protocols.py
├── logs/
│   ├── app.log
│   └── error.log
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## File Responsibilities

- `main.py`: CLI entry point and user interaction loop
- `app/config.py`: loads and validates application settings from environment variables
- `app/prompts.py`: stores default system prompt values
- `app/llm_client.py`: wraps the OpenAI client and sends chat messages to the model
- `app/chat_service.py`: handles input validation, conversation history, and chat workflow
- `app/protocols.py`: defines protocol interfaces for better decoupling
- `app/logger.py`: configures console and file logging
- `app/api/chat_router.py`: API router scaffold prepared for FastAPI migration
- `logs/`: stores runtime logs

## Tech Stack

- Python
- OpenAI Python SDK
- python-dotenv
- standard logging module

## Setup

Create and activate a virtual environment.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4.1-mini
SYSTEM_PROMPT=You are a helpful AI assistant.
```

Notes:

- `OPENAI_API_KEY` is required
- `OPENAI_MODEL` can be changed to another supported model
- `SYSTEM_PROMPT` is optional if a default prompt is defined in code

## How to Run

Run the CLI application:

```bash
python main.py
```

Then interact in the terminal:

```text
You: What is RAG?
AI: RAG stands for Retrieval-Augmented Generation...
```

Type `exit` or `quit` to stop the application.

## Example Usage

Example conversation:

```text
You: What is prompt engineering?
AI: Prompt engineering is the process of designing and refining instructions for language models.

You: Why is it important?
AI: It is important because better prompts can improve output quality, control format, and reduce ambiguity.
```

## Logging

The project uses structured logging for both development and debugging.

Current logging outputs include:

- console logs for runtime monitoring
- `logs/app.log` for general application logs
- `logs/error.log` for error-only logs

## Multi-turn Conversation

The application maintains conversation history in the `ChatService` layer.

This means each new user message can be added to the message history and passed to the model as context, instead of treating every question as a completely independent request.

A simple context window strategy is being used / is planned to avoid sending unlimited chat history and wasting tokens.

## Design Notes

This project is intentionally split into layers:

- configuration layer
- model client layer
- business service layer
- CLI entry layer

The purpose is to keep the code easy to understand now and easy to extend later.

This structure is meant to support future upgrades such as:

- FastAPI API service
- RAG pipeline
- tool calling
- better memory and context management

## Current Limitations

At the current stage:

- the main interface is still CLI-based
- FastAPI routing is only scaffolded, not the main runtime entry yet
- no persistent storage is used for chat history
- no token counting or cost tracking yet
- no RAG pipeline yet

## Next Steps

Planned next steps include:

- turn the CLI workflow into a FastAPI service
- expose a `/chat` API endpoint
- improve request/response schema design
- continue refining conversation history handling
- prepare the codebase for a future RAG extension

## Learning Goals of This Week

This week focused on:

- understanding Python project structure
- calling an LLM API from Python
- separating config, service, and client responsibilities
- adding logging
- understanding how multi-turn context works in practice

## Author

Built as part of a 12-week AI application engineering learning roadmap.