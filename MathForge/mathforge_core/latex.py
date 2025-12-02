"""
LaTeX 输出模块
将AST转换为LaTeX格式，兼容MathJax渲染
"""

from .ast import Node, Number, Symbol, Add, Mul, Pow, Function


def to_latex(node: Node) -> str:
    """
    将AST节点转换为LaTeX字符串
    
    Args:
        node: AST节点
        
    Returns:
        LaTeX格式字符串
    """
    if isinstance(node, Number):
        if node.value == int(node.value):
            return str(int(node.value))
        return str(node.value)
    
    elif isinstance(node, Symbol):
        return node.name
    
    elif isinstance(node, Add):
        terms = []
        for i, term in enumerate(node.terms):
            term_latex = to_latex(term)
            # 处理负号
            if i > 0 and not term_latex.startswith('-'):
                terms.append(' + ' + term_latex)
            elif i > 0:
                terms.append(' ' + term_latex)
            else:
                terms.append(term_latex)
        return ''.join(terms)
    
    elif isinstance(node, Mul):
        factors = []
        for i, factor in enumerate(node.factors):
            factor_latex = to_latex(factor)
            
            # 处理负数
            if isinstance(factor, Number) and factor.value < 0:
                if i == 0:
                    factors.append(factor_latex)
                else:
                    factors.append(f' \\cdot {factor_latex}')
                continue
            
            # 处理需要括号的情况
            needs_parens = isinstance(factor, (Add, Pow)) or isinstance(factor, Function)
            
            if i == 0:
                if needs_parens:
                    factors.append(f'\\left({factor_latex}\\right)')
                else:
                    factors.append(factor_latex)
            else:
                if needs_parens:
                    factors.append(f' \\cdot \\left({factor_latex}\\right)')
                else:
                    # 检查是否需要显式的乘号
                    if isinstance(factor, Number) or isinstance(factor, Symbol):
                        factors.append(f' \\cdot {factor_latex}')
                    else:
                        factors.append(f' {factor_latex}')
        
        result = ''.join(factors)
        # 简化：如果第一个因子是1，去掉
        if result.startswith('1 \\cdot '):
            result = result[9:]
        return result
    
    elif isinstance(node, Pow):
        base_latex = to_latex(node.base)
        exp_latex = to_latex(node.exponent)
        
        # 处理底数需要括号的情况
        if isinstance(node.base, (Add, Mul, Pow)) or isinstance(node.base, Function):
            base_latex = f'\\left({base_latex}\\right)'
        
        # 处理分数指数
        if isinstance(node.exponent, Number):
            exp_val = node.exponent.value
            if abs(exp_val - 0.5) < 1e-10:
                return f'\\sqrt{{{to_latex(node.base)}}}'
            elif abs(exp_val + 0.5) < 1e-10:
                return f'\\frac{{1}}{{\\sqrt{{{to_latex(node.base)}}}}}'
            elif exp_val < 0:
                # 负指数
                abs_exp = abs(exp_val)
                if abs_exp == int(abs_exp):
                    return f'\\frac{{1}}{{{base_latex}^{{{int(abs_exp)}}}}}'
                else:
                    return f'\\frac{{1}}{{{base_latex}^{{{exp_latex}}}}}'
            elif exp_val != int(exp_val):
                # 分数指数
                return f'{base_latex}^{{{exp_latex}}}'
        
        # 处理分数形式的指数（如 1/2）
        if isinstance(node.exponent, Mul):
            # 检查是否是 1/n 形式
            factors = node.exponent.factors
            if len(factors) == 2:
                if factors[0] == Number(1) and isinstance(factors[1], Number):
                    n = factors[1].value
                    if n > 0 and n == int(n):
                        if n == 2:
                            return f'\\sqrt{{{to_latex(node.base)}}}'
                        else:
                            return f'\\sqrt[{int(n)}]{{{to_latex(node.base)}}}'
        
        return f'{base_latex}^{{{exp_latex}}}'
    
    elif isinstance(node, Function):
        func_name = node.name
        arg_latex = to_latex(node.arg)
        
        # 特殊函数名称映射
        func_map = {
            'sin': '\\sin',
            'cos': '\\cos',
            'tan': '\\tan',
            'exp': 'e^{',
            'log': '\\ln',
            'sqrt': '\\sqrt'
        }
        
        latex_name = func_map.get(func_name, func_name)
        
        if func_name == 'exp':
            return f'{latex_name}{arg_latex}}}'
        elif func_name == 'sqrt':
            return f'{latex_name}{{{arg_latex}}}'
        else:
            return f'{latex_name}\\left({arg_latex}\\right)'
    
    else:
        return str(node)
