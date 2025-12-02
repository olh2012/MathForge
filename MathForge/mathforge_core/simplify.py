"""
代数化简模块
"""

from typing import List, Dict
from .ast import Node, Number, Add, Mul, Pow, Symbol, Function


def simplify(node: Node) -> Node:
    """
    化简表达式
    
    Args:
        node: 要化简的AST节点
        
    Returns:
        化简后的AST节点
    """
    # 递归化简子节点
    if isinstance(node, Add):
        return _simplify_add(node)
    elif isinstance(node, Mul):
        return _simplify_mul(node)
    elif isinstance(node, Pow):
        return _simplify_pow(node)
    elif isinstance(node, Function):
        return type(node)(simplify(node.arg))
    else:
        return node


def _simplify_add(add_node: Add) -> Node:
    """化简加法"""
    terms: List[Node] = []
    constant = 0.0
    
    # 展开所有项并收集常数
    for term in add_node.terms:
        simplified = simplify(term)
        
        if isinstance(simplified, Number):
            constant += simplified.value
        elif isinstance(simplified, Mul):
            # 检查是否是 -1 * something
            if len(simplified.factors) == 2:
                if simplified.factors[0] == Number(-1):
                    terms.append(Mul(Number(-1), simplified.factors[1]))
                    continue
                elif simplified.factors[1] == Number(-1):
                    terms.append(Mul(Number(-1), simplified.factors[0]))
                    continue
            terms.append(simplified)
        else:
            terms.append(simplified)
    
    # 合并同类项
    term_dict: Dict[str, Node] = {}
    for term in terms:
        key = _get_term_key(term)
        if key in term_dict:
            term_dict[key] = _combine_terms(term_dict[key], term)
        else:
            term_dict[key] = term
    
    # 重新构建项列表
    new_terms: List[Node] = []
    for term in term_dict.values():
        if isinstance(term, Number) and term.value == 0:
            continue
        new_terms.append(term)
    
    # 添加常数项
    if abs(constant) > 1e-10:
        new_terms.append(Number(constant))
    
    # 如果只有一项，直接返回
    if len(new_terms) == 0:
        return Number(0)
    elif len(new_terms) == 1:
        return new_terms[0]
    
    return Add(*new_terms)


def _simplify_mul(mul_node: Mul) -> Node:
    """化简乘法"""
    factors: List[Node] = []
    constant = 1.0
    
    for factor in mul_node.factors:
        simplified = simplify(factor)
        
        if isinstance(simplified, Number):
            if simplified.value == 0:
                return Number(0)
            constant *= simplified.value
        else:
            factors.append(simplified)
    
    # 展开乘法（如果可能）
    if len(factors) == 0:
        return Number(constant)
    elif len(factors) == 1:
        if abs(constant - 1.0) < 1e-10:
            return factors[0]
        return Mul(Number(constant), factors[0])
    
    if abs(constant - 1.0) > 1e-10:
        factors.insert(0, Number(constant))
    
    return Mul(*factors)


def _simplify_pow(pow_node: Pow) -> Node:
    """化简幂次"""
    base = simplify(pow_node.base)
    exponent = simplify(pow_node.exponent)
    
    # x^0 = 1
    if isinstance(exponent, Number) and abs(exponent.value) < 1e-10:
        return Number(1)
    
    # x^1 = x
    if isinstance(exponent, Number) and abs(exponent.value - 1.0) < 1e-10:
        return base
    
    # 0^x = 0 (x > 0)
    if isinstance(base, Number) and abs(base.value) < 1e-10:
        if isinstance(exponent, Number) and exponent.value > 0:
            return Number(0)
    
    # 1^x = 1
    if isinstance(base, Number) and abs(base.value - 1.0) < 1e-10:
        return Number(1)
    
    # (a^b)^c = a^(b*c)
    if isinstance(base, Pow):
        new_exp = simplify(Mul(base.exponent, exponent))
        return Pow(base.base, new_exp)
    
    return Pow(base, exponent)


def _get_term_key(term: Node) -> str:
    """获取项的键用于合并同类项"""
    if isinstance(term, Mul):
        # 提取非常数因子
        non_const = [f for f in term.factors if not isinstance(f, Number)]
        if non_const:
            return str(sorted([str(f) for f in non_const]))
        return "constant"
    elif isinstance(term, Pow):
        return str(term)
    elif isinstance(term, Symbol):
        return str(term)
    elif isinstance(term, Function):
        return str(term)
    else:
        return "constant"


def _combine_terms(term1: Node, term2: Node) -> Node:
    """合并两个同类项"""
    # 提取系数
    coef1 = _extract_coefficient(term1)
    coef2 = _extract_coefficient(term2)
    
    # 提取非系数部分
    base1 = _extract_base(term1)
    base2 = _extract_base(term2)
    
    if base1 == base2:
        new_coef = coef1 + coef2
        if abs(new_coef) < 1e-10:
            return Number(0)
        if abs(new_coef - 1.0) < 1e-10:
            return base1
        return Mul(Number(new_coef), base1)
    
    return Add(term1, term2)


def _extract_coefficient(term: Node) -> float:
    """提取项的系数"""
    if isinstance(term, Number):
        return term.value
    elif isinstance(term, Mul):
        for factor in term.factors:
            if isinstance(factor, Number):
                return factor.value
        return 1.0
    else:
        return 1.0


def _extract_base(term: Node) -> Node:
    """提取项的非系数部分"""
    if isinstance(term, Number):
        return Number(1)
    elif isinstance(term, Mul):
        non_const = [f for f in term.factors if not isinstance(f, Number)]
        if non_const:
            if len(non_const) == 1:
                return non_const[0]
            return Mul(*non_const)
        return Number(1)
    else:
        return term
