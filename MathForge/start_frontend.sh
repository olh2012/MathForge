#!/bin/bash
# 启动前端服务

cd "$(dirname "$0")/frontend"
npm install
npm run dev
