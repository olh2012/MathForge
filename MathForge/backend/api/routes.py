"""
FastAPI 路由定义
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from mathforge_core import parse, simplify, diff, integrate, solve, to_latex, Symbol

router = APIRouter()


class ExpressionRequest(BaseModel):
    expression: str
    variable: Optional[str] = 'x'


class SimplifyRequest(BaseModel):
    expression: str


class DiffRequest(BaseModel):
    expression: str
    variable: str = 'x'


class IntegrateRequest(BaseModel):
    expression: str
    variable: str = 'x'


class SolveRequest(BaseModel):
    expression: str
    variable: str = 'x'


class EvalRequest(BaseModel):
    expression: str
    values: Dict[str, float] = {}


@router.post("/simplify")
async def simplify_expression(request: SimplifyRequest):
    """化简表达式"""
    try:
        expr = parse(request.expression)
        simplified = simplify(expr)
        return {
            "result": str(simplified),
            "latex": to_latex(simplified),
            "ast": _ast_to_dict(simplified)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/latex")
async def to_latex_endpoint(request: SimplifyRequest):
    """转换为LaTeX"""
    try:
        expr = parse(request.expression)
        simplified = simplify(expr)
        return {
            "result": str(simplified),
            "latex": to_latex(simplified),
            "ast": _ast_to_dict(simplified)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/diff")
async def differentiate(request: DiffRequest):
    """求导"""
    try:
        expr = parse(request.expression)
        var = Symbol(request.variable)
        derivative = diff(expr, var)
        simplified = simplify(derivative)
        return {
            "result": str(simplified),
            "latex": to_latex(simplified),
            "ast": _ast_to_dict(simplified)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/integrate")
async def integrate_endpoint(request: IntegrateRequest):
    """积分"""
    try:
        expr = parse(request.expression)
        var = Symbol(request.variable)
        integral = integrate(expr, var)
        simplified = simplify(integral)
        return {
            "result": str(simplified),
            "latex": to_latex(simplified),
            "ast": _ast_to_dict(simplified)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve")
async def solve_endpoint(request: SolveRequest):
    """求解方程"""
    try:
        expr = parse(request.expression)
        var = Symbol(request.variable)
        solutions = solve(expr, var)
        return {
            "result": [str(sol) for sol in solutions],
            "latex": [to_latex(sol) for sol in solutions],
            "count": len(solutions),
            "ast": [_ast_to_dict(sol) for sol in solutions]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/eval")
async def evaluate(request: EvalRequest):
    """数值求值"""
    try:
        expr = parse(request.expression)
        simplified = simplify(expr)
        result = simplified.eval(request.values)
        return {
            "result": str(result),
            "value": result,
            "latex": str(result)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def _ast_to_dict(node) -> Dict[str, Any]:
    """将AST节点转换为字典（用于JSON序列化）"""
    if isinstance(node, (Symbol, Number)):
        return {
            "type": type(node).__name__,
            "value": node.name if isinstance(node, Symbol) else node.value
        }
    elif isinstance(node, (Add, Mul)):
        return {
            "type": type(node).__name__,
            "children": [_ast_to_dict(child) for child in (node.terms if isinstance(node, Add) else node.factors)]
        }
    elif isinstance(node, Pow):
        return {
            "type": "Pow",
            "base": _ast_to_dict(node.base),
            "exponent": _ast_to_dict(node.exponent)
        }
    elif isinstance(node, Function):
        return {
            "type": type(node).__name__,
            "name": node.name,
            "arg": _ast_to_dict(node.arg)
        }
    else:
        return {"type": "Unknown", "value": str(node)}
