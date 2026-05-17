def get_tool_definitions() -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": "calculate_expression",
                "description": "Calculate a simple arithmetic expression.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "A simple arithmetic expression, such as '12 * 8 + 3'.",
                        }
                    },
                    "required": ["expression"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_knowledge_base",
                "description": "Search the local RAG knowledge base for relevant project information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The search query.",
                        },
                        "top_k": {
                            "type": "integer",
                            "description": "Number of chunks to retrieve.",
                        },
                    },
                    "required": ["question"],
                    "additionalProperties": False,
                },
            },
        },
    ]