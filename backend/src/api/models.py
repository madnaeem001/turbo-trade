from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class UploadResponse(BaseModel):
    filename: str
    size: int
    status: str

class StartOptimizationRequest(BaseModel):
    csv_file: str
    mode: str = Field(default="OPTIMIZATION", pattern="^(OPTIMIZATION|LIVE)$")

    strategies: List[str] = Field(default_factory=lambda: ["sma_crossover", "rsi_oversold"])
    duration_seconds: Optional[int] = None

class ResultsResponse(BaseModel):
    status: str
    pnl: Dict[str, float]
    avg_latency_ms: float
    total_ticks: int
    total_trades: int
    execution_time_sec: float
    trades: List[Dict[str, Any]]

class MetricsUpdate(BaseModel):
    status: str
    pnl: Dict[str, float]
    avg_latency_ms: float
    total_ticks: int
    trades_executed: int
    timestamp: str