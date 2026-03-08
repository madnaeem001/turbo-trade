import multiprocessing
import time
from typing import Callable
from functools import wraps

class ConcurrencyController:
    """Manages locks for safe concurrent access to shared state"""
    
    def __init__(self):
        self.pnl_lock = multiprocessing.Lock()
        self.trade_log_lock = multiprocessing.Lock()
        self.latency_lock = multiprocessing.Lock()
        self.state_lock = multiprocessing.Lock()
    
    def atomic_pnl_update(self, func: Callable) -> Callable:
        """Decorator for atomic P&L updates"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.pnl_lock:
                return func(*args, **kwargs)
        return wrapper
    
    def atomic_trade_log(self, func: Callable) -> Callable:
        """Decorator for atomic trade log updates"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.trade_log_lock:
                return func(*args, **kwargs)
        return wrapper
    
    def acquire_pnl_lock(self):
        """Context manager for P&L lock"""
        return self.pnl_lock
    
    def acquire_trade_log_lock(self):
        """Context manager for trade log lock"""
        return self.trade_log_lock
    
    def acquire_latency_lock(self):
        """Context manager for latency lock"""
        return self.latency_lock
