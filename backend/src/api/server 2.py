from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import logging
from ..config import settings
from .routes import router
from .websocket import websocket_handler, ws_manager
from ..core import ExecutionEngine

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create app
app = FastAPI(
    title="TurboTrade API",
    description="Parallel HFT Backtesting Engine",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
engine: Optional[ExecutionEngine] = None

def init_app():
    """Initialize application"""
    global engine
    engine = ExecutionEngine()
    logger.info("ExecutionEngine initialized")

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    init_app()
    logger.info("TurboTrade API started")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("TurboTrade API shutdown")

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "TurboTrade",
        "version": "1.0.0",
        "status": "running"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics"""
    await websocket_handler(websocket, engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
