import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """Global configuration for TurboTrade"""
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Execution Engine
    NUM_WORKER_PROCESSES: int = 4
    NUM_DATA_PRODUCERS: int = 1
    TICK_PROCESSING_RATE: int = 1000  # ticks/second
    STRATEGY_TIMEOUT: int = 60
    
    # Queue Settings
    MAX_QUEUE_SIZE: int = 10000
    QUEUE_TIMEOUT: int = 30
    
    # Redis Configuration
    USE_REDIS: bool = True
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_TIMEOUT: int = 5
    
    # Server Configuration
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    UVICORN_WORKERS: int = 4
    RELOAD: bool = True
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_DIR: Path = BASE_DIR / "logs"
    LOG_FILE: str = "turbotrade.log"
    
    # Data Configuration
    DATA_DIR: Path = BASE_DIR / "data"
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100 MB
    CHUNK_SIZE: int = 1024
    
    # Performance Settings
    BENCHMARK_SERIAL: bool = True
    LATENCY_MEASUREMENT: bool = True
    MEASURE_INTERVAL: float = 0.1  # seconds
    
    # Strategy Configuration
    MAX_STRATEGIES: int = 10
    DEFAULT_STRATEGIES: list = [
        "sma_crossover",
        "rsi_oversold",
        "momentum",
        "volume_spike"
    ]
    
    # WebSocket Configuration
    WS_HEARTBEAT_INTERVAL: float = 0.5  # seconds
    WS_MAX_SIZE: int = 1024 * 1024  # 1 MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Create required directories
settings.LOG_DIR.mkdir(parents=True, exist_ok=True)
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)