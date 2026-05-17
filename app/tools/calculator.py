from __future__ import annotations
import operator
import ast

_ALLOWED_OPERATORS = {
    ast.Add : operator.add,
    ast.Sub : operator.sub,
    ast.Mult : operator.mul,
    ast.Div : operator.truediv,
    ast.Pow : operator.pow,
    ast.USub : operator.neg,
}

def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        return _ALLOWED_OPERATORS[type(node.op)](left, right)
        
        
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        operand = _eval_node(node.operand)
        # In this case, node.op is ast.Usub, need to be return so the father node can treat this exp as negative constant
        return _ALLOWED_OPERATORS[type(node.op)](operand)

    raise ValueError(f"Unsupported expression: {ast.dump(node, indent=4)}")

def calculate_expression(expression: str) -> str:
    expression = expression.strip()

    if not expression:
        raise ValueError("Expression cannot be empty.")
    
    tree = ast.parse(expression, mode="eval")
    result = _eval_node(tree.body)
    return str(result)