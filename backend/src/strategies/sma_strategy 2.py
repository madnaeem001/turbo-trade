from typing import Dict, Any, Optional
from .base_strategy import BaseStrategy

class SMAStrategy(BaseStrategy):
    """
    Simple Moving Average Crossover Strategy
    Signals:
    - BUY when fast SMA crosses above slow SMA
    - SELL when fast SMA crosses below slow SMA
    """
    
    def __init__(self, strategy_id: str, fast_period: int = 5, slow_period: int = 20):
        super().__init__(strategy_id, window_size=slow_period + 5)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.last_signal = None
    
    def evaluate(self, tick: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Evaluate tick for SMA crossover signals"""
        self.add_tick(tick)
        
        if len(self.price_history) < self.slow_period:
            return None
        
        fast_sma = self.calculate_sma(self.fast_period)
        slow_sma = self.calculate_sma(self.slow_period)
        
        if fast_sma is None or slow_sma is None:
            return None
        
        current_signal = "BUY" if fast_sma > slow_sma else "SELL"
        
        # Generate signal on crossover
        if self.last_signal is None:
            self.last_signal = current_signal
            return None
        
        if self.last_signal != current_signal:
            self.last_signal = current_signal
            self.trades_count += 1
            
            return {
                "strategy_id": self.strategy_id,
                "side": current_signal,
                "quantity": 10,  # Fixed quantity
                "price": tick["price"],
                "reason": f"SMA({self.fast_period}) crossover SMA({self.slow_period})"
            }
        
        return None