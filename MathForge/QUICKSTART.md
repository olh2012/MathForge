# MathForge 快速开始指南

## 快速启动

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend
npm install
cd ..
```

### 2. 启动服务

**方式一：使用启动脚本**

```bash
# 终端1：启动后端
./start_backend.sh

# 终端2：启动前端
./start_frontend.sh
```

**方式二：手动启动**

```bash
# 终端1：启动后端
cd backend
python main.py
# 或
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 终端2：启动前端
cd frontend
npm run dev
```

### 3. 访问应用

- **前端界面**: http://localhost:5173
- **后端API文档**: http://localhost:8000/docs
- **API根路径**: http://localhost:8000

## 使用 CLI

```bash
python -m cli.main
# 或
python cli/main.py
```

## 运行示例

```bash
python examples/example.py
```

## 测试 API

```bash
# 化简表达式
curl -X POST http://localhost:8000/api/simplify \
  -H "Content-Type: application/json" \
  -d '{"expression": "x^2 + 2*x + x"}'

# 求导
curl -X POST http://localhost:8000/api/diff \
  -H "Content-Type: application/json" \
  -d '{"expression": "x^2 + 3*x", "variable": "x"}'

# 积分
curl -X POST http://localhost:8000/api/integrate \
  -H "Content-Type: application/json" \
  -d '{"expression": "x^2", "variable": "x"}'

# 求解方程
curl -X POST http://localhost:8000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"expression": "x^2 - 4", "variable": "x"}'
```

## 支持的表达式示例

- `x^2 + 2*x + 1` - 多项式
- `sin(x)^2 + cos(x)^2` - 三角函数
- `exp(x) * log(x)` - 指数和对数
- `sqrt(x^2 + 1)` - 平方根
- `(x + 1) * (x - 1)` - 括号表达式

## 常见问题

### 端口被占用

如果 8000 或 5173 端口被占用，可以修改：

- **后端端口**: 编辑 `backend/main.py` 中的 `port=8000`
- **前端端口**: 编辑 `frontend/vite.config.js` 中的 `port: 5173`

### 导入错误

确保在项目根目录运行命令，或使用：

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 前端无法连接后端

检查 `frontend/vite.config.js` 中的代理配置，确保后端地址正确。
