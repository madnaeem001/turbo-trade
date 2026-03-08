from typing import Dict, Any, Optional
from .base_strategy import BaseStrategy

class MomentumStrategy(BaseStrategy):
    """
    Price Momentum Strategy
    Signals:
    - BUY when momentum is positive and increasing
    - SELL when momentum is negative and decreasing
    """
    
    def __init__(self, strategy_id: str, period: int = 10, threshold: float = 0):
        super().__init__(strategy_id, window_size=period + 5)
        self.period = period
        self.threshold = threshold
        self.last_momentum = 0
    
    def evaluate(self, tick: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Evaluate tick for momentum signals"""
        self.add_tick(tick)
        
        if len(self.price_history) < self.period + 1:
            return None
        
        momentum = self.calculate_momentum(self.period)
        
        if momentum is None:
            return None
        
        signal = None
        
        # Momentum crossing threshold
        if self.last_momentum <= self.threshold < momentum:
            signal = "BUY"
        elif self.last_momentum > self.threshold >= momentum:
            signal = "SELL"
        
        self.last_momentum = momentum
        
        if signal:
            self.trades_count += 1
            return {
                "strategy_id": self.strategy_id,
                "side": signal,
                "quantity": 10,
                "price": tick["price"],
                "reason": f"Momentum({momentum:.2f}) threshold crossover"
            }
        
        return None