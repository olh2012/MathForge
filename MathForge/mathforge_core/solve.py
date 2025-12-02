"""
求解器模块：求解方程
"""

from typing import List, Optional
from .ast import Node, Number, Symbol, Add, Mul, Pow
from .simplify import simplify


def solve(equation: Node, var: Symbol) -> List[Node]:
    """
    求解方程 equation = 0
    
    Args:
        equation: 方程表达式（已移项，等于0）
        var: 要求解的变量
        
    Returns:
        解的列表
    """
    from .rewrite import rewrite
    
    # 化简方程
    equation = simplify(equation)
    
    # 尝试线性方程: ax + b = 0
    solution = _solve_linear(equation, var)
    if solution is not None:
        return [solution]
    
    # 尝试二次方程: ax^2 + bx + c = 0
    solutions = _solve_quadratic(equation, var)
    if solutions:
        return solutions
    
    # 尝试简单多项式
    solutions = _solve_polynomial(equation, var)
    if solutions:
        return solutions
    
    # 无法求解
    return []


def _solve_linear(equation: Node, var: Symbol) -> Optional[Node]:
    """求解线性方程 ax + b = 0"""
    # 将方程转换为 Add 形式
    if not isinstance(equation, Add):
        if isinstance(equation, Mul):
            # 可能是 a*x 形式
            equation = Add(equation, Number(0))
        elif isinstance(equation, Symbol):
            if equation == var:
                return Number(0)
            return None
        elif isinstance(equation, Number):
            if abs(equation.value) < 1e-10:
                return var  # 0 = 0，所有值都是解
            return None
        else:
            return None
    
    # 收集包含 var 的项和常数项
    var_coef = Number(0)
    constant = Number(0)
    
    for term in equation.terms:
        coef = _extract_var_coefficient(term, var)
        if coef is not None:
            var_coef = Add(var_coef, coef)
        else:
            # 常数项（取负，因为移项）
            const_val = _extract_constant(term)
            constant = Add(constant, Mul(Number(-1), const_val))
    
    # ax + b = 0 => x = -b/a
    if isinstance(var_coef, Number) and abs(var_coef.value) < 1e-10:
        # 系数为0
        if isinstance(constant, Number) and abs(constant.value) < 1e-10:
            return var  # 0 = 0
        return None  # 无解
    
    # 计算解
    if isinstance(var_coef, Number) and isinstance(constant, Number):
        if abs(var_coef.value) < 1e-10:
            return None
        solution = Number(-constant.value / var_coef.value)
        return simplify(solution)
    
    # 符号计算
    solution = Mul(Number(-1), Mul(constant, Pow(var_coef, Number(-1))))
    return simplify(solution)


def _solve_quadratic(equation: Node, var: Symbol) -> List[Node]:
    """求解二次方程 ax^2 + bx + c = 0"""
    from .simplify import simplify
    
    if not isinstance(equation, Add):
        return []
    
    # 提取系数
    a = Number(0)
    b = Number(0)
    c = Number(0)
    
    for term in equation.terms:
        coef_a = _extract_power_coefficient(term, var, 2)
        if coef_a is not None:
            a = Add(a, coef_a)
            continue
        
        coef_b = _extract_power_coefficient(term, var, 1)
        if coef_b is not None:
            b = Add(b, coef_b)
            continue
        
        # 常数项
        # 方程已经是 expr = 0 形式，常数项直接使用其值
        const_val = _extract_constant(term)
        if isinstance(const_val, Number) and abs(const_val.value) > 1e-10:
            c = Add(c, const_val)
    
    # 化简系数
    a = simplify(a)
    b = simplify(b)
    c = simplify(c)
    
    # 检查是否是二次方程
    if isinstance(a, Number) and abs(a.value) < 1e-10:
        return []  # 不是二次方程
    
    # 使用求根公式: x = (-b ± sqrt(b^2 - 4ac)) / (2a)
    if isinstance(a, Number) and isinstance(b, Number) and isinstance(c, Number):
        discriminant = b.value ** 2 - 4 * a.value * c.value
        
        if discriminant < 0:
            return []  # 无实数解
        
        sqrt_disc = discriminant ** 0.5
        two_a = 2 * a.value
        
        x1 = Number((-b.value + sqrt_disc) / two_a)
        x2 = Number((-b.value - sqrt_disc) / two_a)
        
        if abs(x1.value - x2.value) < 1e-10:
            return [x1]
        
        return [x1, x2]
    
    return []


def _solve_polynomial(equation: Node, var: Symbol) -> List[Node]:
    """求解简单多项式（尝试因式分解）"""
    # 这里只实现基础功能
    # 实际应用中需要更复杂的算法
    return []


def _extract_var_coefficient(term: Node, var: Symbol) -> Optional[Node]:
    """提取项中变量的系数"""
    if isinstance(term, Symbol):
        if term == var:
            return Number(1)
        return None
    
    if isinstance(term, Mul):
        # 查找包含 var 的因子
        var_found = False
        coef = Number(1)
        
        for factor in term.factors:
            if factor == var:
                var_found = True
            elif isinstance(factor, Number):
                coef = Mul(coef, factor)
            elif isinstance(factor, Pow) and factor.base == var:
                var_found = True
                if isinstance(factor.exponent, Number) and factor.exponent.value == 1:
                    pass
                else:
                    return None  # 不是线性项
        
        if var_found:
            return simplify(coef)
    
    if isinstance(term, Pow) and term.base == var:
        if isinstance(term.exponent, Number) and term.exponent.value == 1:
            return Number(1)
    
    return None


def _extract_power_coefficient(term: Node, var: Symbol, power: int) -> Optional[Node]:
    """提取特定幂次的系数"""
    # 直接是 x^n 形式
    if isinstance(term, Pow) and term.base == var:
        if isinstance(term.exponent, Number) and abs(term.exponent.value - power) < 1e-10:
            return Number(1)
        return None
    
    # x^1 = x
    if term == var and power == 1:
        return Number(1)
    
    # 乘法形式: a * x^n
    if isinstance(term, Mul):
        var_found = False
        coef = Number(1)
        
        for factor in term.factors:
            if isinstance(factor, Pow) and factor.base == var:
                if isinstance(factor.exponent, Number) and abs(factor.exponent.value - power) < 1e-10:
                    var_found = True
                else:
                    return None
            elif factor == var and power == 1:
                var_found = True
            elif isinstance(factor, Number):
                coef = Mul(coef, factor)
            elif isinstance(factor, Mul):
                # 处理嵌套的乘法（如 -1 * 4）
                if len(factor.factors) == 2 and isinstance(factor.factors[0], Number):
                    coef = Mul(coef, factor)
            else:
                return None
        
        if var_found:
            return simplify(coef)
    
    return None


def _extract_constant(term: Node) -> Node:
    """提取常数项（不包含变量的项）"""
    from .ast import Symbol, Pow
    
    # 检查项是否包含变量
    def has_variable(node: Node) -> bool:
        if isinstance(node, Symbol):
            return True
        elif isinstance(node, Pow):
            return has_variable(node.base)
        elif isinstance(node, (Add, Mul)):
            children = node.terms if isinstance(node, Add) else node.factors
            return any(has_variable(child) for child in children)
        elif hasattr(node, 'arg'):  # Function
            return has_variable(node.arg)
        return False
    
    # 如果包含变量，返回 None（通过返回 Number(0) 表示不是常数）
    if has_variable(term):
        return Number(0)
    
    # 提取数值
    if isinstance(term, Number):
        return term
    
    if isinstance(term, Mul):
        # 检查是否所有因子都是常数
        all_const = True
        const_val = 1.0
        for factor in term.factors:
            if isinstance(factor, Number):
                const_val *= factor.value
            else:
                all_const = False
                break
        
        if all_const:
            return Number(const_val)
    
    # 其他情况返回 0（表示不是常数项）
    return Number(0)
