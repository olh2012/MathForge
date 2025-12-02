"""
重写规则系统
实现模式匹配和替换
"""

from typing import Dict, Optional
from .ast import Node, Number, Symbol, Add, Mul, Pow, Function, Sin, Cos


def rewrite(node: Node, rules: Optional[Dict[str, Node]] = None) -> Node:
    """
    应用重写规则
    
    Args:
        node: 要重写的AST节点
        rules: 重写规则字典（可选，使用默认规则）
        
    Returns:
        重写后的节点
    """
    if rules is None:
        rules = _default_rules()
    
    # 递归应用规则
    result = node
    changed = True
    max_iterations = 100
    iteration = 0
    
    while changed and iteration < max_iterations:
        changed = False
        iteration += 1
        
        for pattern, replacement in rules.items():
            new_result = _apply_rule(result, pattern, replacement)
            if new_result != result:
                result = new_result
                changed = True
                break
    
    return result


def _default_rules() -> Dict[str, Node]:
    """默认重写规则"""
    from .parser import parse
    
    rules = {}
    
    # sin^2(x) + cos^2(x) = 1
    x = Symbol('x')
    rules['trig_identity'] = parse('sin(x)^2 + cos(x)^2')
    
    return rules


def _apply_rule(node: Node, pattern: str, replacement: Node) -> Node:
    """应用单个重写规则"""
    # 这里实现简化的模式匹配
    # 实际应用中需要更复杂的模式匹配算法
    
    # 检查是否是 sin^2 + cos^2 形式
    if isinstance(node, Add):
        sin_squared = None
        cos_squared = None
        
        for term in node.terms:
            if isinstance(term, Pow):
                if isinstance(term.base, Sin):
                    if isinstance(term.exponent, Number) and abs(term.exponent.value - 2) < 1e-10:
                        sin_squared = term
                elif isinstance(term.base, Cos):
                    if isinstance(term.exponent, Number) and abs(term.exponent.value - 2) < 1e-10:
                        cos_squared = term
        
        if sin_squared and cos_squared:
            # 检查参数是否相同
            if sin_squared.base.arg == cos_squared.base.arg:
                return Number(1)
    
    # 递归应用到子节点
    if isinstance(node, Add):
        return Add(*[_apply_rule(term, pattern, replacement) for term in node.terms])
    elif isinstance(node, Mul):
        return Mul(*[_apply_rule(factor, pattern, replacement) for factor in node.factors])
    elif isinstance(node, Pow):
        return Pow(_apply_rule(node.base, pattern, replacement),
                  _apply_rule(node.exponent, pattern, replacement))
    elif isinstance(node, Function):
        return type(node)(_apply_rule(node.arg, pattern, replacement))
    
    return node
