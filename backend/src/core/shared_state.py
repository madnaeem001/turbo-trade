import multiprocessing
from typing import Dict, Any, List
import json
from datetime import datetime

class SharedState:
    """Manages shared state across multiple processes using multiprocessing.Manager()"""
    
    def __init__(self):
        self.manager = multiprocessing.Manager()
        
        # Shared dictionaries and lists
        self.state = self.manager.dict()
        self.pnl = self.manager.dict()
        self.latencies = self.manager.list()
        self.trade_log = self.manager.list()
        self.strategy_metrics = self.manager.dict()
        
        # Initialize
        self._initialize_state()
    
    def _initialize_state(self):
        """Initialize shared state dictionaries"""
        self.state["status"] = "IDLE"
        self.state["mode"] = "OPTIMIZATION"
        self.state["total_ticks_processed"] = 0
        self.state["errors"] = 0
        self.state["start_time"] = None
        self.state["end_time"] = None
    
    def get_pnl(self, strategy_id: str) -> float:
        """Get P&L for a specific strategy"""
        return self.pnl.get(strategy_id, 0.0)
    
    def update_pnl(self, strategy_id: str, amount: float):
        """Update P&L (thread-safe when used with locks)"""
        current = self.pnl.get(strategy_id, 0.0)
        self.pnl[strategy_id] = current + amount
    
    def set_pnl(self, strategy_id: str, amount: float):
        """Set absolute P&L value"""
        self.pnl[strategy_id] = amount
    
    def add_latency(self, latency_ms: float):
        """Record latency measurement"""
        self.latencies.append(latency_ms)
    
    def get_avg_latency(self) -> float:
        """Calculate average latency"""
        if not self.latencies:
            return 0.0
        return sum(self.latencies) / len(self.latencies)
    
    def add_trade(self, trade_data: Dict[str, Any]):
        """Log trade execution"""
        trade_data["timestamp"] = datetime.now().isoformat()
        self.trade_log.append(trade_data)
    
    def get_trades(self, limit: int = 100) -> List[Dict]:
        """Get last N trades"""
        return list(self.trade_log)[-limit:]
    
    def set_status(self, status: str):
        """Update execution status"""
        self.state["status"] = status
    
    def get_status(self) -> str:
        """Get current status"""
        return self.state.get("status", "IDLE")
    
    def increment_tick_count(self, count: int = 1):
        """Increment total ticks processed"""
        current = self.state.get("total_ticks_processed", 0)
        self.state["total_ticks_processed"] = current + count
    
    def get_tick_count(self) -> int:
        """Get total ticks processed"""
        return self.state.get("total_ticks_processed", 0)
    
    def get_all_pnl(self) -> Dict[str, float]:
        """Get all P&L values"""
        return dict(self.pnl)
    
    def get_snapshot(self) -> Dict[str, Any]:
        """Get complete state snapshot"""
        return {
            "status": self.get_status(),
            "pnl": self.get_all_pnl(),
            "avg_latency": self.get_avg_latency(),
            "total_ticks": self.get_tick_count(),
            "trade_count": len(self.trade_log),
            "timestamp": datetime.now().isoformat()
        }