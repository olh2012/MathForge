# MathForge 符号数学系统

一个完整的符号数学系统，类似 Maple / Mathematica / SymPy，包含符号数学核心引擎、LaTeX 输出、Web UI 和命令行工具。

## 项目结构

```
MathForge/
├── backend/              # FastAPI 后端
│   ├── main.py          # 主应用
│   └── api/
│       └── routes.py    # API 路由
├── frontend/            # Vue 3 前端
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   └── components/
│   │       └── MathInput.vue
│   ├── package.json
│   └── vite.config.js
├── mathforge_core/      # 符号数学核心引擎
│   ├── __init__.py
│   ├── ast.py          # AST 节点定义
│   ├── parser.py       # 表达式解析器
│   ├── simplify.py     # 代数化简
│   ├── calculus.py     # 微积分（求导、积分）
│   ├── solve.py        # 方程求解
│   ├── latex.py        # LaTeX 输出
│   └── rewrite.py      # 重写规则系统
├── cli/                 # 命令行工具
│   └── main.py
├── examples/            # 示例代码
│   └── example.py
├── requirements.txt     # Python 依赖
└── README.md
```

## 功能特性

### 符号数学核心引擎

- **表达式系统（AST）**: 支持符号、数字、加法、乘法、幂次、函数等节点
- **表达式解析器**: 将字符串表达式解析为 AST
- **代数化简**: 常数折叠、乘法展开、合并同类项、幂次规则
- **微积分**: 符号求导和基础积分
- **方程求解**: 支持线性方程和二次方程
- **LaTeX 输出**: 完整的 LaTeX 格式输出，兼容 MathJax
- **数值求值**: 支持变量替换和数值计算

### Web API (FastAPI)

- `POST /api/simplify` - 化简表达式
- `POST /api/latex` - 转换为 LaTeX
- `POST /api/diff` - 符号求导
- `POST /api/integrate` - 符号积分
- `POST /api/solve` - 求解方程
- `POST /api/eval` - 数值求值

### Web UI (Vue 3)

- 表达式输入框
- 功能按钮：Simplify、Derivative、Integral、Solve、To LaTeX
- MathJax 渲染 LaTeX 结果
- 简洁美观的界面

### CLI 工具

交互式命令行界面，支持所有核心功能。

## 安装与运行

### 1. 安装 Python 依赖

```bash
cd MathForge
pip install -r requirements.txt
```

### 2. 启动后端服务

```bash
cd backend
python main.py
```

或者使用 uvicorn：

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

后端将在 `http://localhost:8000` 启动。

### 3. 启动前端服务

```bash
cd frontend
npm install
npm run dev
```

前端将在 `http://localhost:5173` 启动（Vite 默认端口）。

### 4. 使用 CLI 工具

```bash
python -m cli.main
```

或者：

```bash
python cli/main.py
```

## 使用示例

### Python API 示例

```python
from mathforge_core import parse, simplify, diff, integrate, solve, to_latex, Symbol

# 解析表达式
expr = parse("x^2 + 2*x + 1")

# 化简
simplified = simplify(expr)
print(simplified)  # x^2 + 2*x + 1

# 求导
x = Symbol('x')
derivative = simplify(diff(expr, x))
print(derivative)  # 2*x + 2

# 积分
integral = simplify(integrate(expr, x))
print(integral)  # x^3/3 + x^2 + x

# 求解方程
solutions = solve(parse("x^2 - 4"), x)
print(solutions)  # [2.0, -2.0]

# LaTeX 输出
print(to_latex(expr))  # x^{2} + 2 \cdot x + 1
```

### CLI 示例

```
mathforge> simplify x^2 + 2*x + x
结果: x^2 + 3*x
LaTeX: x^{2} + 3 \cdot x

mathforge> diff x^2 + 3*x x
导数: 2*x + 3
LaTeX: 2 \cdot x + 3

mathforge> integrate x^2 x
积分: x^3/3
LaTeX: \frac{x^{3}}{3}

mathforge> solve x^2 - 4 x
解: 2.0, -2.0
LaTeX: 2.0, -2.0
```

### Web API 示例

```bash
# 化简表达式
curl -X POST http://localhost:8000/api/simplify \
  -H "Content-Type: application/json" \
  -d '{"expression": "x^2 + 2*x + x"}'

# 求导
curl -X POST http://localhost:8000/api/diff \
  -H "Content-Type: application/json" \
  -d '{"expression": "x^2 + 3*x", "variable": "x"}'
```

## 支持的表达式语法

- **数字**: `123`, `3.14`, `-5`
- **变量**: `x`, `y`, `a`, `b`
- **运算符**: `+`, `-`, `*`, `/`, `^` (幂次)
- **函数**: `sin(x)`, `cos(x)`, `tan(x)`, `exp(x)`, `log(x)`, `sqrt(x)`
- **括号**: `(x + 1) * 2`

## 技术栈

- **后端**: Python 3 + FastAPI
- **前端**: Vue 3 + Vite + MathJax
- **符号引擎**: 纯 Python 实现（无外部 CAS 库依赖）

## 开发说明

### 运行示例

```bash
python examples/example.py
```

### 测试核心功能

```python
from mathforge_core import parse, simplify, to_latex

# 测试解析
expr = parse("sin(x)^2 + cos(x)^2")
print(expr)

# 测试化简
result = simplify(expr)
print(result)

# 测试 LaTeX
print(to_latex(result))
```

## 许可证

MIT License

## 作者

MathForge 开发团队
