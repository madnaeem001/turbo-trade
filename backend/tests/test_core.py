import pytest
import multiprocessing
from src.core import ExecutionEngine, OrderMatchingEngine, SharedState
from src.strategies import SMAStrategy, RSIStrategy

@pytest.fixture
def engine():
    return ExecutionEngine()

@pytest.fixture
def ome():
    return OrderMatchingEngine()

def test_shared_state_initialization(engine):
    """Test SharedState initialization"""
    assert engine.shared_state.get_status() == "IDLE"
    assert len(engine.shared_state.get_all_pnl()) == 0

def test_pnl_update(engine):
    """Test P&L updates"""
    engine.shared_state.set_pnl("S1", 100)
    assert engine.shared_state.get_pnl("S1") == 100
    
    engine.shared_state.update_pnl("S1", 50)
    assert engine.shared_state.get_pnl("S1") == 150

def test_ome_order_submission(ome):
    """Test OME order submission"""
    order = ome.submit_order("S1", "AAPL", "BUY", 10, 150)
    assert order.order_id is not None
    assert order.quantity == 10
    assert order.price == 150

def test_ome_order_matching(ome):
    """Test OME order matching"""
    # Submit buy and sell orders
    ome.submit_order("S1", "AAPL", "BUY", 10, 150)
    ome.submit_order("S2", "AAPL", "SELL", 10, 150)

    trades = ome.match_orders()
    assert len(trades) > 0
    assert trades[0].quantity == 10  # <-- Access first trade's quantity


def test_sma_strategy():
    """Test SMA strategy"""
    strategy = SMAStrategy("TEST", fast_period=5, slow_period=20)
    
    for price in range(100, 120):
        tick = {"price": price, "volume": 1000}
        signal = strategy.evaluate(tick)
    
    assert len(strategy.price_history) > 0

def test_rsi_strategy():
    """Test RSI strategy"""
    strategy = RSIStrategy("TEST", period=14)
    
    prices = [100, 101, 102, 101, 100, 99, 98, 97, 98, 99, 100, 101, 102, 103, 104]
    for price in prices:
        tick = {"price": price, "volume": 1000}
        signal = strategy.evaluate(tick)
    
    rsi = strategy.calculate_rsi(14)
    assert rsi is not None
    assert 0 <= rsi <= 100
