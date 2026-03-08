import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import time
from typing import Callable, List, Dict, Any
from .shared_state import SharedState
from .locks import ConcurrencyController
from .ome import OrderMatchingEngine
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class ExecutionEngine:
    """
    Parallel execution engine that manages:
    1. Data producer process
    2. Multiple strategy worker processes
    3. Order matching and execution
    4. Shared state management
    """
    
    def __init__(self):
        self.shared_state = SharedState()
        self.concurrency = ConcurrencyController()
        self.ome = OrderMatchingEngine()
        self.data_queue = multiprocessing.Queue(maxsize=settings.MAX_QUEUE_SIZE)
        self.executor: Optional[ProcessPoolExecutor] = None
        self.start_time = None
        self.end_time = None
    
    def run_simulation(self, 
                      data_producer: Callable,
                      strategy_workers: List[Callable],
                      num_workers: int = settings.NUM_WORKER_PROCESSES):
        """
        Run parallel simulation with multiple strategy workers.
        
        Args:
            data_producer: Function that reads and queues data
            strategy_workers: List of strategy worker functions
            num_workers: Number of parallel worker processes
        """
        self.shared_state.set_status("RUNNING")
        self.start_time = time.time()
        
        try:
            with ProcessPoolExecutor(max_workers=num_workers + 1) as executor:
                self.executor = executor
                
                # Submit data producer
                logger.info("Starting data producer...")
                producer_future = executor.submit(
                    data_producer,
                    self.data_queue,
                    self.shared_state
                )
                
                # Submit strategy workers
                logger.info(f"Starting {num_workers} strategy workers...")
                worker_futures = [
                    executor.submit(
                        worker,
                        self.data_queue,
                        self.shared_state,
                        self.concurrency,
                        self.ome,
                        worker_id
                    )
                    for worker_id, worker in enumerate(strategy_workers[:num_workers])
                ]
                
                # Wait for completion
                producer_future.result()
                for future in worker_futures:
                    future.result()
        
        except Exception as e:
            logger.error(f"Simulation error: {str(e)}")
            self.shared_state.set_status("ERROR")
            raise
        
        finally:
            self.end_time = time.time()
            self.shared_state.set_status("COMPLETED")
            self.executor = None
    
    def process_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an order through the OME (thread-safe).
        Must be called within a lock context!
        """
        try:
            # Submit order
            order = self.ome.submit_order(
                strategy_id=order_data["strategy_id"],
                symbol=order_data.get("symbol", "UNKNOWN"),
                side=order_data["side"],
                quantity=order_data["quantity"],
                price=order_data["price"]
            )
            
            # Try to match
            trades = self.ome.match_orders()
            
            # Update shared state
            for trade in trades:
                with self.concurrency.acquire_pnl_lock():
                    self.shared_state.update_pnl(trade.strategy_id, trade.pnl)
                
                with self.concurrency.acquire_trade_log_lock():
                    self.shared_state.add_trade(trade.to_dict())
                
                with self.concurrency.acquire_latency_lock():
                    self.shared_state.add_latency(trade.latency_ms)
            
            return {
                "status": "SUCCESS",
                "order_id": order.order_id,
                "trades_executed": len(trades)
            }
        
        except Exception as e:
            logger.error(f"Order processing error: {str(e)}")
            return {
                "status": "ERROR",
                "message": str(e)
            }
    
    def get_results(self) -> Dict[str, Any]:
        """Get final simulation results"""
        elapsed_time = (self.end_time - self.start_time) if self.end_time else 0
        
        return {
            "status": self.shared_state.get_status(),
            "pnl": self.shared_state.get_all_pnl(),
            "avg_latency_ms": self.shared_state.get_avg_latency(),
            "total_ticks": self.shared_state.get_tick_count(),
            "total_trades": len(self.ome.executed_trades),
            "execution_time_sec": elapsed_time,
            "trades": self.ome.get_executed_trades()[:100]  # Last 100 trades
        }
    
    def get_live_metrics(self) -> Dict[str, Any]:
        """Get live metrics during execution"""
        return self.shared_state.get_snapshot()