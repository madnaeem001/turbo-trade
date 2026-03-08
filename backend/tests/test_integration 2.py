import pytest
import time
from src.core import ExecutionEngine
from src.data.producer import data_producer
from src.strategies import SMAStrategy

def test_full_simulation():
    """Integration test: Full parallel simulation"""
    engine = ExecutionEngine()
    
    # Create simple test data
    def test_producer(queue, shared_state):
        for i in range(100, 120):
            queue.put({"price": i, "volume": 1000})
        for _ in range(1):
            queue.put("STOP")
    
    def test_worker(queue, shared_state, concurrency, ome, worker_id):
        strategy = SMAStrategy(f"S{worker_id}", fast_period=3, slow_period=5)
        while True:
            tick = queue.get()
            if tick == "STOP":
                break
            signal = strategy.evaluate(tick)
            if signal:
                shared_state.update_pnl(signal['strategy_id'], 10)
    
    # Run simulation
    engine.run_simulation(
        test_producer,
        [test_worker],
        num_workers=1
    )
    
    results = engine.get_results()
    assert results["status"] == "COMPLETED"
    assert results["total_ticks"] > 0
