"""
MathForge 使用示例
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from mathforge_core import parse, simplify, diff, integrate, solve, to_latex, Symbol

print("=" * 60)
print("MathForge 符号数学系统示例")
print("=" * 60)
print()

# 示例1: 解析和化简
print("示例1: 解析和化简")
expr1 = parse("x^2 + 2*x + x + 3")
print(f"原始表达式: x^2 + 2*x + x + 3")
print(f"化简结果: {simplify(expr1)}")
print(f"LaTeX: {to_latex(simplify(expr1))}")
print()

# 示例2: 求导
print("示例2: 求导")
expr2 = parse("x^2 + 3*x + 1")
x = Symbol('x')
derivative = simplify(diff(expr2, x))
print(f"表达式: {expr2}")
print(f"导数: {derivative}")
print(f"LaTeX: {to_latex(derivative)}")
print()

# 示例3: 积分
print("示例3: 积分")
expr3 = parse("x^2 + 2*x")
integral = simplify(integrate(expr3, x))
print(f"表达式: {expr3}")
print(f"积分: {integral}")
print(f"LaTeX: {to_latex(integral)}")
print()

# 示例4: 求解方程
print("示例4: 求解方程")
expr4 = parse("x^2 - 4")
solutions = solve(expr4, x)
print(f"方程: {expr4} = 0")
print(f"解: {solutions}")
for sol in solutions:
    print(f"  - {sol} (LaTeX: {to_latex(sol)})")
print()

# 示例5: 数值求值
print("示例5: 数值求值")
expr5 = parse("x^2 + 2*x + 1")
result = simplify(expr5)
value = result.eval({'x': 3})
print(f"表达式: {expr5}")
print(f"当 x = 3 时，值 = {value}")
print()

# 示例6: 三角函数
print("示例6: 三角函数")
expr6 = parse("sin(x)^2 + cos(x)^2")
print(f"表达式: {expr6}")
print(f"LaTeX: {to_latex(expr6)}")
print()

# 示例7: 复合函数求导
print("示例7: 复合函数求导")
expr7 = parse("sin(x^2)")
derivative7 = simplify(diff(expr7, x))
print(f"表达式: {expr7}")
print(f"导数: {derivative7}")
print(f"LaTeX: {to_latex(derivative7)}")
print()

print("=" * 60)
print("示例完成！")
print("=" * 60)
