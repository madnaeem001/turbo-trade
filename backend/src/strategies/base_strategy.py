from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from collections import deque
import numpy as np

class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    Implements common functionality for indicator calculation.
    """
    
    def __init__(self, strategy_id: str, window_size: int = 20):
        self.strategy_id = strategy_id
        self.window_size = window_size
        self.price_history = deque(maxlen=window_size)
        self.volume_history = deque(maxlen=window_size)
        self.position = 0  # 0: flat, 1: long, -1: short
        self.entry_price = 0
        self.trades_count = 0
    
    @abstractmethod
    def evaluate(self, tick: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Evaluate tick and return order if signal generated.
        
        Args:
            tick: Market tick data with 'price', 'volume', 'timestamp'
        
        Returns:
            Order dict with 'side', 'quantity', 'price' or None
        """
        pass
    
    def add_tick(self, tick: Dict[str, Any]):
        """Add price tick to history"""
        self.price_history.append(tick["price"])
        self.volume_history.append(tick.get("volume", 0))
    
    def get_price_history(self) -> np.ndarray:
        """Get price history as numpy array"""
        return np.array(list(self.price_history))
    
    def get_volume_history(self) -> np.ndarray:
        """Get volume history as numpy array"""
        return np.array(list(self.volume_history))
    
    def calculate_sma(self, period: int) -> Optional[float]:
        """Calculate Simple Moving Average"""
        if len(self.price_history) < period:
            return None
        prices = self.get_price_history()
        return np.mean(prices[-period:])
    
    def calculate_ema(self, period: int) -> Optional[float]:
        """Calculate Exponential Moving Average"""
        if len(self.price_history) < period:
            return None
        prices = self.get_price_history()
        ema = prices[0]
        multiplier = 2.0 / (period + 1)
        for price in prices[1:]:
            ema = price * multiplier + ema * (1 - multiplier)
        return ema
    
    def calculate_rsi(self, period: int = 14) -> Optional[float]:
        """Calculate Relative Strength Index"""
        if len(self.price_history) < period + 1:
            return None
        prices = self.get_price_history()
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        if avg_loss == 0:
            return 100 if avg_gain > 0 else 50
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_momentum(self, period: int = 10) -> Optional[float]:
        """Calculate Price Momentum"""
        if len(self.price_history) < period + 1:
            return None
        prices = self.get_price_history()
        return prices[-1] - prices[-period-1]
    
    def calculate_bollinger_bands(self, period: int = 20, std_dev: float = 2.0):
        """Calculate Bollinger Bands"""
        if len(self.price_history) < period:
            return None
        prices = self.get_price_history()
        sma = np.mean(prices[-period:])
        std = np.std(prices[-period:])
        return {
            "upper": sma + (std * std_dev),
            "middle": sma,
            "lower": sma - (std * std_dev)
        }
    
    def should_open_position(self, signal: str) -> bool:
        """Check if should open new position"""
        return self.position == 0 and signal in ["BUY", "SELL"]
    
    def should_close_position(self, signal: str) -> bool:
        """Check if should close existing position"""
        return self.position != 0 and ((self.position > 0 and signal == "SELL") or (self.position < 0 and signal == "BUY"))