import pytest

from app.tools.calculator import calculate_expression

def test_calculate_expression_addition():
    assert calculate_expression("1+2") == "3"

def test_calculate_expression_operator_priority():
    assert calculate_expression("12 * 4 + 6") ==  "54"

def test_calculate_expression_parentheses():
    assert calculate_expression("(2 + 3) * 3") == "15"

def test_calculate_expression_negative_number():
    assert calculate_expression("-5 + 2") == "-3"


def test_calculate_expression_empty_input():
    with pytest.raises(ValueError):
        calculate_expression("   ")


def test_calculate_expression_rejects_function_call():
    with pytest.raises(ValueError):
        calculate_expression("max(1, 2)")


def test_calculate_expression_rejects_unsafe_code():
    with pytest.raises(ValueError):
        calculate_expression("__import__('os').system('ls')")