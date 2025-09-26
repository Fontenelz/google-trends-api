# src/trends/main.py
import uvicorn
from fastapi import FastAPI
from .routes import router as trends_router
from .scheduler import start_scheduler

def create_app() -> FastAPI:
    app = FastAPI(title="Google Trends API")

    @app.on_event("startup")
    async def startup_event():
        start_scheduler()
        print("iniciado")

    app.include_router(trends_router, prefix="")
    return app
    
def main():
    uvicorn.run(
        "trends.main:create_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
