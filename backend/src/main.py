import multiprocessing
import logging
from .core import ExecutionEngine
from .data.producer import data_producer
from .strategies import (SMAStrategy, RSIStrategy, MomentumStrategy, VolumeStrategy)
from .config import settings
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def strategy_worker_wrapper(worker_id: int, strategy_class, strategy_args):
    """Wrapper for strategy worker"""
    def worker(data_queue, shared_state, concurrency, ome, worker_id):
        strategy = strategy_class(**strategy_args)
        
        while True:
            try:
                tick = data_queue.get(timeout=5)
                
                if tick == "STOP":
                    break
                
                # Evaluate strategy
                order = strategy.evaluate(tick)
                
                if order:
                    # Process order through OME
                    with concurrency.acquire_pnl_lock():
                        result = engine.process_order(order)
            
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {str(e)}")
                break
    
    return worker

def run_parallel_simulation(csv_path: str = None):
    """Run parallel simulation"""
    logger.info("Starting TurboTrade Parallel Simulation")
    
    if csv_path is None:
        csv_path = settings.DATA_DIR / "sample_data.csv"
    
    # Create engine
    engine = ExecutionEngine()
    
    # Create strategy workers
    strategy_configs = [
        (SMAStrategy, {"strategy_id": "S1", "fast_period": 5, "slow_period": 20}),
        (RSIStrategy, {"strategy_id": "S2", "period": 14}),
        (MomentumStrategy, {"strategy_id": "S3", "period": 10}),
        (VolumeStrategy, {"strategy_id": "S4", "window": 20}),
    ]
    
    strategy_workers = [
        strategy_worker_wrapper(i, cls, args)
        for i, (cls, args) in enumerate(strategy_configs)
    ]
    
    # Run simulation
    try:
        engine.run_simulation(
            data_producer,
            strategy_workers,
            num_workers=settings.NUM_WORKER_PROCESSES
        )
        
        results = engine.get_results()
        logger.info(f"Simulation complete: {results}")
        return results
    
    except Exception as e:
        logger.error(f"Simulation error: {str(e)}")
        raise

if __name__ == "__main__":
    # For Windows multiprocessing
    multiprocessing.set_start_method("spawn", force=True)
    results = run_parallel_simulation()