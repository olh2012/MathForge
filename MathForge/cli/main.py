"""
MathForge 命令行工具
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from mathforge_core import parse, simplify, diff, integrate, solve, to_latex, Symbol


def print_help():
    """打印帮助信息"""
    print("""
MathForge 符号数学系统 CLI

命令:
  simplify <expr>      - 化简表达式
  latex <expr>         - 转换为LaTeX
  diff <expr> [var]    - 求导（默认变量: x）
  integrate <expr> [var] - 积分（默认变量: x）
  solve <expr> [var]   - 求解方程（默认变量: x）
  eval <expr> [var=val] - 数值求值
  help                 - 显示此帮助
  exit                 - 退出

示例:
  simplify x^2 + 2*x + x
  diff x^2 + 3*x x
  integrate x^2 x
  solve x^2 - 4 x
  eval x^2 + 1 x=2
""")


def parse_eval_args(args):
    """解析求值命令的参数"""
    expr = args[0]
    values = {}
    
    for arg in args[1:]:
        if '=' in arg:
            var, val = arg.split('=', 1)
            values[var.strip()] = float(val.strip())
    
    return expr, values


def main():
    """主函数"""
    print("MathForge CLI v1.0.0")
    print("输入 'help' 查看帮助，'exit' 退出")
    print()
    
    while True:
        try:
            line = input("mathforge> ").strip()
            
            if not line:
                continue
            
            if line == "exit" or line == "quit":
                print("再见！")
                break
            
            if line == "help":
                print_help()
                continue
            
            parts = line.split()
            if not parts:
                continue
            
            cmd = parts[0]
            args = parts[1:]
            
            if cmd == "simplify":
                if not args:
                    print("错误: 需要表达式")
                    continue
                expr_str = ' '.join(args)
                expr = parse(expr_str)
                result = simplify(expr)
                print(f"结果: {result}")
                print(f"LaTeX: {to_latex(result)}")
            
            elif cmd == "latex":
                if not args:
                    print("错误: 需要表达式")
                    continue
                expr_str = ' '.join(args)
                expr = parse(expr_str)
                result = simplify(expr)
                print(f"LaTeX: {to_latex(result)}")
            
            elif cmd == "diff":
                if not args:
                    print("错误: 需要表达式")
                    continue
                expr_str = args[0]
                var_name = args[1] if len(args) > 1 else 'x'
                expr = parse(expr_str)
                var = Symbol(var_name)
                result = simplify(diff(expr, var))
                print(f"导数: {result}")
                print(f"LaTeX: {to_latex(result)}")
            
            elif cmd == "integrate":
                if not args:
                    print("错误: 需要表达式")
                    continue
                expr_str = args[0]
                var_name = args[1] if len(args) > 1 else 'x'
                expr = parse(expr_str)
                var = Symbol(var_name)
                result = simplify(integrate(expr, var))
                print(f"积分: {result}")
                print(f"LaTeX: {to_latex(result)}")
            
            elif cmd == "solve":
                if not args:
                    print("错误: 需要表达式")
                    continue
                expr_str = args[0]
                var_name = args[1] if len(args) > 1 else 'x'
                expr = parse(expr_str)
                var = Symbol(var_name)
                solutions = solve(expr, var)
                if solutions:
                    print(f"解: {', '.join(str(s) for s in solutions)}")
                    print(f"LaTeX: {', '.join(to_latex(s) for s in solutions)}")
                else:
                    print("无解或无法求解")
            
            elif cmd == "eval":
                if not args:
                    print("错误: 需要表达式")
                    continue
                expr_str, values = parse_eval_args(args)
                expr = parse(expr_str)
                result = simplify(expr)
                try:
                    value = result.eval(values)
                    print(f"值: {value}")
                except Exception as e:
                    print(f"错误: {e}")
            
            else:
                print(f"未知命令: {cmd}")
                print("输入 'help' 查看帮助")
        
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    main()
