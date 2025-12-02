# MathForge 项目总结

## 项目概述

MathForge 是一个完整的符号数学系统，类似 Maple / Mathematica / SymPy，完全使用纯 Python 实现，不依赖外部 CAS 库。

## 已实现功能

### ✅ 符号数学核心引擎

1. **表达式系统（AST）**
   - Node, Symbol, Number, Add, Mul, Pow, Function
   - Sin, Cos, Tan, Exp, Log, Sqrt 函数节点
   - 完整的运算符重载（+, -, *, /, **）

2. **表达式解析器**
   - Lexer（词法分析器）
   - Parser（递归下降语法分析器）
   - 支持：数字、变量、运算符、函数、括号

3. **代数化简**
   - 常数折叠
   - 乘法展开
   - 合并同类项
   - 幂次规则

4. **微积分**
   - 符号求导（支持链式法则、乘积法则）
   - 基础积分（多项式、简单函数）

5. **方程求解**
   - 线性方程求解
   - 二次方程求解（求根公式）

6. **LaTeX 输出**
   - 完整的 LaTeX 格式转换
   - 兼容 MathJax 渲染
   - 支持分数、幂次、函数、括号等

7. **数值求值**
   - 变量替换
   - 数值计算

### ✅ Web API (FastAPI)

- `POST /api/simplify` - 化简表达式
- `POST /api/latex` - 转换为 LaTeX
- `POST /api/diff` - 符号求导
- `POST /api/integrate` - 符号积分
- `POST /api/solve` - 求解方程
- `POST /api/eval` - 数值求值

### ✅ Web UI (Vue 3)

- 表达式输入界面
- 功能按钮：Simplify、Derivative、Integral、Solve、LaTeX
- MathJax 实时渲染
- 美观的现代化界面（Element Plus）

### ✅ CLI 工具

交互式命令行界面，支持所有核心功能。

## 项目结构

```
MathForge/
├── backend/              # FastAPI 后端
│   ├── main.py
│   └── api/
│       └── routes.py
├── frontend/            # Vue 3 前端
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   └── components/
│   ├── package.json
│   └── vite.config.js
├── mathforge_core/      # 符号数学核心引擎
│   ├── ast.py          # AST 节点
│   ├── parser.py       # 解析器
│   ├── simplify.py     # 化简
│   ├── calculus.py     # 微积分
│   ├── solve.py        # 求解器
│   ├── latex.py        # LaTeX 输出
│   └── rewrite.py      # 重写规则
├── cli/                 # CLI 工具
│   └── main.py
├── examples/            # 示例代码
│   └── example.py
├── requirements.txt
├── README.md
└── QUICKSTART.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

### 2. 启动服务

```bash
# 终端1：启动后端
./start_backend.sh
# 或
cd backend && python main.py

# 终端2：启动前端
./start_frontend.sh
# 或
cd frontend && npm run dev
```

### 3. 访问应用

- 前端：http://localhost:5173
- API文档：http://localhost:8000/docs

## 使用示例

### Python API

```python
from mathforge_core import parse, simplify, diff, integrate, solve, to_latex, Symbol

# 解析和化简
expr = parse("x^2 + 2*x + x")
result = simplify(expr)

# 求导
x = Symbol('x')
derivative = simplify(diff(expr, x))

# 积分
integral = simplify(integrate(parse("x^2"), x))

# 求解
solutions = solve(parse("x^2 - 4"), x)

# LaTeX
latex_str = to_latex(result)
```

### CLI

```
mathforge> simplify x^2 + 2*x + x
结果: x^2 + 3*x

mathforge> diff x^2 + 3*x x
导数: 2*x + 3

mathforge> solve x^2 - 4 x
解: 2.0, -2.0
```

### Web API

```bash
curl -X POST http://localhost:8000/api/simplify \
  -H "Content-Type: application/json" \
  -d '{"expression": "x^2 + 2*x + x"}'
```

## 技术栈

- **后端**: Python 3 + FastAPI
- **前端**: Vue 3 + Vite + Element Plus + MathJax
- **符号引擎**: 纯 Python 实现

## 测试结果

所有核心功能已测试通过：
- ✅ 表达式解析
- ✅ 代数化简
- ✅ 符号求导
- ✅ 符号积分
- ✅ 方程求解（线性、二次）
- ✅ LaTeX 输出
- ✅ 数值求值

## 文件清单

### 核心引擎（8个文件）
- `mathforge_core/__init__.py`
- `mathforge_core/ast.py` (约 300 行)
- `mathforge_core/parser.py` (约 200 行)
- `mathforge_core/simplify.py` (约 200 行)
- `mathforge_core/calculus.py` (约 150 行)
- `mathforge_core/solve.py` (约 250 行)
- `mathforge_core/latex.py` (约 150 行)
- `mathforge_core/rewrite.py` (约 80 行)

### 后端（3个文件）
- `backend/__init__.py`
- `backend/main.py`
- `backend/api/routes.py`

### 前端（5个文件）
- `frontend/index.html`
- `frontend/package.json`
- `frontend/vite.config.js`
- `frontend/src/main.js`
- `frontend/src/App.vue`

### 其他（5个文件）
- `cli/main.py`
- `examples/example.py`
- `requirements.txt`
- `README.md`
- `QUICKSTART.md`

**总计**: 约 25 个文件，约 3000+ 行代码

## 项目特点

1. **完全自主实现**：不依赖 SymPy 或其他 CAS 库
2. **全栈系统**：包含后端、前端、CLI 完整实现
3. **LaTeX 支持**：完整的 LaTeX 输出和 MathJax 渲染
4. **可扩展性**：模块化设计，易于扩展新功能
5. **文档完整**：包含 README、快速开始指南、示例代码

## 后续可扩展功能

- 更多函数支持（asin, acos, atan 等）
- 更复杂的积分（分部积分、换元积分）
- 更高级的求解器（高次多项式、方程组）
- 符号矩阵运算
- 级数展开
- 极限计算

## 许可证

MIT License

---

**项目完成时间**: 2024年12月
**状态**: ✅ 完整可用
