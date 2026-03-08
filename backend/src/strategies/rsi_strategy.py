from typing import Dict, Any, Optional
from .base_strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    """
    Relative Strength Index Strategy
    Signals:
    - BUY when RSI oversold (< 30)
    - SELL when RSI overbought (> 70)
    """
    
    def __init__(self, strategy_id: str, period: int = 14, oversold: float = 30, overbought: float = 70):
        super().__init__(strategy_id, window_size=period + 5)
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        self.last_signal = None
    
    def evaluate(self, tick: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Evaluate tick for RSI signals"""
        self.add_tick(tick)
        
        if len(self.price_history) < self.period + 1:
            return None
        
        rsi = self.calculate_rsi(self.period)
        
        if rsi is None:
            return None
        
        signal = None
        if rsi < self.oversold:
            signal = "BUY"
        elif rsi > self.overbought:
            signal = "SELL"
        
        if signal and signal != self.last_signal:
            self.last_signal = signal
            self.trades_count += 1
            
            return {
                "strategy_id": self.strategy_id,
                "side": signal,
                "quantity": 10,
                "price": tick["price"],
                "reason": f"RSI({rsi:.2f}) at extremum"
            }
        
        return None