#!/bin/bash
# 启动后端服务

cd "$(dirname "$0")"
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
