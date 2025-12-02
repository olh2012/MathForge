"""
FastAPI 主应用
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router

app = FastAPI(title="MathForge API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api", tags=["math"])


@app.get("/")
async def root():
    return {
        "message": "MathForge API",
        "version": "1.0.0",
        "endpoints": [
            "POST /api/simplify",
            "POST /api/latex",
            "POST /api/diff",
            "POST /api/integrate",
            "POST /api/solve",
            "POST /api/eval"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
