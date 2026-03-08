import time
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class OrderSide(str, Enum):
    """Order side enumeration"""
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(str, Enum):
    """Order status enumeration"""
    PENDING = "PENDING"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

@dataclass
class Order:
    """Represents a trading order"""
    order_id: str
    strategy_id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    timestamp: float
    
    def to_dict(self):
        return asdict(self)

@dataclass
class Trade:
    """Represents an executed trade"""
    trade_id: str
    order_id: str
    strategy_id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    execution_price: float
    pnl: float
    timestamp: float
    latency_ms: float
    
    def to_dict(self):
        return asdict(self)

class OrderMatchingEngine:
    """
    Implements deterministic order matching with FIFO price-time priority.
    This is the critical synchronization point for all concurrent orders.
    
    All operations must be protected by locks to ensure:
    1. Deterministic execution (same order every time)
    2. Data integrity (no race conditions)
    3. Fair price-time priority matching
    """
    
    def __init__(self):
        self.order_book: Dict[str, List[Order]] = {
            "BUY": [],
            "SELL": []
        }
        self.executed_trades: List[Trade] = []
        self.order_counter = 0
        self.trade_counter = 0
    
    def submit_order(self, strategy_id: str, symbol: str, side: str, 
                    quantity: float, price: float) -> Order:
        """
        Submit order to matching engine.
        Must be called within a lock context!
        """
        self.order_counter += 1
        order_id = f"ORD-{self.order_counter}"
        
        order = Order(
            order_id=order_id,
            strategy_id=strategy_id,
            symbol=symbol,
            side=OrderSide(side),
            quantity=quantity,
            price=price,
            timestamp=time.time()
        )
        
        # Add to order book
        side_key = "BUY" if side == "BUY" else "SELL"
        self.order_book[side_key].append(order)
        
        return order
    
    def match_orders(self) -> List[Trade]:
        """
        Match standing orders using price-time priority.
        Returns list of executed trades.
        """
        trades = []
        
        while self._can_match():
            best_buy = self._get_best_order("BUY")
            best_sell = self._get_best_order("SELL")
            
            if not best_buy or not best_sell:
                break
            
            # Check if prices cross
            if best_buy.price >= best_sell.price:
                # Execute trade at sell price (price-time priority)
                trade = self._execute_trade(best_buy, best_sell)
                trades.append(trade)
                self.executed_trades.append(trade)
                
                # Remove matched orders
                self.order_book["BUY"].remove(best_buy)
                self.order_book["SELL"].remove(best_sell)
            else:
                break
        
        return trades
    
    def _can_match(self) -> bool:
        """Check if there are orders to match"""
        return len(self.order_book["BUY"]) > 0 and len(self.order_book["SELL"]) > 0
    
    def _get_best_order(self, side: str) -> Optional[Order]:
        """Get best order (highest buy or lowest sell) with price-time priority"""
        orders = self.order_book[side]
        if not orders:
            return None
        
        if side == "BUY":
            # Sort by price (desc) then timestamp (asc)
            return max(orders, key=lambda o: (o.price, -o.timestamp))
        else:
            # Sort by price (asc) then timestamp (asc)
            return min(orders, key=lambda o: (o.price, o.timestamp))
    
    def _execute_trade(self, buy_order: Order, sell_order: Order) -> Trade:
        """Execute a matched pair of orders"""
        self.trade_counter += 1
        
        execution_price = sell_order.price  # Sell price priority
        quantity = min(buy_order.quantity, sell_order.quantity)
        
        # Calculate P&L (simplified - long position profit)
        pnl = (execution_price - buy_order.price) * quantity
        
        trade = Trade(
            trade_id=f"TRD-{self.trade_counter}",
            order_id=buy_order.order_id,
            strategy_id=buy_order.strategy_id,
            symbol=buy_order.symbol,
            side=OrderSide.BUY,
            quantity=quantity,
            price=buy_order.price,
            execution_price=execution_price,
            pnl=pnl,
            timestamp=time.time(),
            latency_ms=(time.time() - buy_order.timestamp) * 1000
        )
        
        return trade
    
    def get_executed_trades(self) -> List[Dict]:
        """Get all executed trades"""
        return [trade.to_dict() for trade in self.executed_trades]
    
    def get_pending_orders(self) -> Dict[str, List[Dict]]:
        """Get pending orders"""
        return {
            "BUY": [order.to_dict() for order in self.order_book["BUY"]],
            "SELL": [order.to_dict() for order in self.order_book["SELL"]]
        }
