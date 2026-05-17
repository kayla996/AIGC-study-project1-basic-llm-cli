import json
from typing import Any

from pydantic import ValidationError

from app.rag.rag_core import RAGCore
from app.tools.calculator import calculate_expression
from app.tools.rag_tools import search_knowledge_base
from app.tools.schemas import CalculatorArgs, KnowledgeBaseSearchArgs,ToolExecutionResult

class ToolExecutor:
    def __init__(self, rag_core: RAGCore) -> None:
        self._rag_core = rag_core

    def execute(self, tool_name: str, arguments: str | dict[str, Any]) -> ToolExecutionResult:
        try:
            raw_args = self._parse_arguments(arguments)

            if tool_name == "calculate_expression":
                args = CalculatorArgs.model_validate(raw_args)
                result = calculate_expression(args.expression)

                return ToolExecutionResult(
                    tool_name=tool_name, 
                    success=True,
                    result=result,
                    raw=raw_args)
            
            elif tool_name == "search_knowledge_base":
                args = KnowledgeBaseSearchArgs.model_validate(raw_args)
                result = search_knowledge_base(self._rag_core, args.question, args.top_k)

                return ToolExecutionResult(
                    tool_name=tool_name,
                    success=True,
                    result=result.model_dump(),
                    raw=raw_args
                )
            raise ValueError(f"Unknown tool: {tool_name}")

        except ValidationError as exc:
            return ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                error=f"Invalid tool arguments: {exc}"
            )
        
        except Exception as exc:
            return ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                error=str(exc)
            )

    def _parse_arguments(self, arguments: str | dict[str, Any]) -> dict[str, Any]:
        if isinstance(arguments, str):
            return json.loads(arguments or "{}")
        
        return arguments