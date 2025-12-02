"""
微积分模块：符号求导和积分
"""

from .ast import Node, Number, Symbol, Add, Mul, Pow, Function, Sin, Cos, Tan, Exp, Log, Sqrt


def diff(node: Node, var: Symbol) -> Node:
    """
    对表达式求导
    
    Args:
        node: 要求导的AST节点
        var: 对哪个变量求导
        
    Returns:
        导数表达式
    """
    if isinstance(node, Number):
        return Number(0)
    
    elif isinstance(node, Symbol):
        if node == var:
            return Number(1)
        else:
            return Number(0)
    
    elif isinstance(node, Add):
        return Add(*[diff(term, var) for term in node.terms])
    
    elif isinstance(node, Mul):
        # 乘积法则: (f*g)' = f'*g + f*g'
        if len(node.factors) == 2:
            f, g = node.factors
            return Add(
                Mul(diff(f, var), g),
                Mul(f, diff(g, var))
            )
        else:
            # 多个因子的乘积法则
            result = Number(0)
            for i in range(len(node.factors)):
                terms = list(node.factors)
                terms[i] = diff(terms[i], var)
                result = Add(result, Mul(*terms))
            return result
    
    elif isinstance(node, Pow):
        base = node.base
        exponent = node.exponent
        
        # 如果指数是常数
        if isinstance(exponent, Number):
            # (x^n)' = n*x^(n-1)
            if isinstance(base, Symbol) and base == var:
                if exponent.value == 1:
                    return Number(1)
                new_exp = Number(exponent.value - 1)
                if abs(new_exp.value) < 1e-10:
                    return Number(1)
                return Mul(exponent, Pow(base, new_exp))
            else:
                # (f^n)' = n*f^(n-1)*f'
                new_exp = Number(exponent.value - 1)
                if abs(new_exp.value) < 1e-10:
                    return Mul(exponent, diff(base, var))
                return Mul(exponent, Mul(Pow(base, new_exp), diff(base, var)))
        else:
            # 一般情况: (f^g)' = f^g * (g*ln(f))'
            # 简化处理：假设指数不依赖变量
            if isinstance(exponent, Number):
                return diff(Pow(base, exponent), var)
            else:
                # 复杂情况，简化处理
                return Mul(node, Add(
                    Mul(diff(exponent, var), Log(base)),
                    Mul(exponent, Mul(Pow(base, Number(-1)), diff(base, var)))
                ))
    
    elif isinstance(node, Sin):
        # (sin(f))' = cos(f) * f'
        return Mul(Cos(node.arg), diff(node.arg, var))
    
    elif isinstance(node, Cos):
        # (cos(f))' = -sin(f) * f'
        return Mul(Number(-1), Mul(Sin(node.arg), diff(node.arg, var)))
    
    elif isinstance(node, Tan):
        # (tan(f))' = sec^2(f) * f' = (1 + tan^2(f)) * f'
        return Mul(Add(Number(1), Pow(Tan(node.arg), Number(2))), diff(node.arg, var))
    
    elif isinstance(node, Exp):
        # (e^f)' = e^f * f'
        return Mul(Exp(node.arg), diff(node.arg, var))
    
    elif isinstance(node, Log):
        # (ln(f))' = f' / f
        return Mul(diff(node.arg, var), Pow(node.arg, Number(-1)))
    
    elif isinstance(node, Sqrt):
        # (sqrt(f))' = f' / (2*sqrt(f))
        return Mul(diff(node.arg, var), Mul(Number(0.5), Pow(node.arg, Number(-0.5))))
    
    else:
        # 未知函数，返回未化简的导数形式
        return node


def integrate(node: Node, var: Symbol) -> Node:
    """
    对表达式积分（基础多项式积分）
    
    Args:
        node: 要积分的AST节点
        var: 对哪个变量积分
        
    Returns:
        积分表达式
    """
    from .simplify import simplify
    
    # 常数积分
    if isinstance(node, Number):
        return Mul(node, var)
    
    # 变量积分
    if isinstance(node, Symbol):
        if node == var:
            return Mul(Number(0.5), Pow(var, Number(2)))
        else:
            return Mul(node, var)
    
    # 加法积分
    if isinstance(node, Add):
        return Add(*[integrate(term, var) for term in node.terms])
    
    # 常数乘以函数
    if isinstance(node, Mul):
        # 检查是否有常数因子
        constants = [f for f in node.factors if isinstance(f, Number)]
        non_constants = [f for f in node.factors if not isinstance(f, Number)]
        
        if constants:
            const_value = 1.0
            for c in constants:
                const_value *= c.value
            if non_constants:
                return Mul(Number(const_value), integrate(Mul(*non_constants), var))
            else:
                return Mul(Number(const_value), var)
    
    # 幂次积分: x^n -> x^(n+1)/(n+1)
    if isinstance(node, Pow):
        if node.base == var and isinstance(node.exponent, Number):
            exp_val = node.exponent.value
            if abs(exp_val + 1) < 1e-10:
                # 1/x 的积分是 ln(x)
                return Log(var)
            new_exp = Number(exp_val + 1)
            return Mul(Pow(var, new_exp), Pow(new_exp, Number(-1)))
    
    # 简单函数积分
    if isinstance(node, Sin):
        if node.arg == var:
            return Mul(Number(-1), Cos(var))
    
    if isinstance(node, Cos):
        if node.arg == var:
            return Sin(var)
    
    if isinstance(node, Exp):
        if node.arg == var:
            return Exp(var)
    
    # 无法积分的情况，返回原表达式（实际应用中应抛出异常）
    return simplify(node)
