from typing import Dict, Any, Optional
import numpy as np
from .base_strategy import BaseStrategy

class VolumeStrategy(BaseStrategy):
    """
    Volume Spike Strategy
    Signals:
    - BUY when volume spikes above average and price rises
    - SELL when volume spikes above average and price falls
    """
    
    def __init__(self, strategy_id: str, window: int = 20, multiplier: float = 1.5):
        super().__init__(strategy_id, window_size=window + 5)
        self.window = window
        self.multiplier = multiplier
        self.last_volume = 0
    
    def evaluate(self, tick: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Evaluate tick for volume spike signals"""
        self.add_tick(tick)
        
        if len(self.volume_history) < self.window:
            return None
        
        volumes = self.get_volume_history()
        avg_volume = np.mean(volumes[:-1])  # Exclude current
        current_volume = volumes[-1]
        
        if current_volume < avg_volume * self.multiplier:
            return None
        
        # Volume spike detected
        prices = self.get_price_history()
        price_direction = "UP" if prices[-1] > prices[-2] else "DOWN"
        
        signal = "BUY" if price_direction == "UP" else "SELL"
        
        self.trades_count += 1
        
        return {
            "strategy_id": self.strategy_id,
            "side": signal,
            "quantity": 10,
            "price": tick["price"],
            "reason": f"Volume spike ({current_volume / avg_volume:.1f}x avg)"
        }