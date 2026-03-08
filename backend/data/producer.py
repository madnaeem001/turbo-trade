import multiprocessing
import time
import logging
from typing import Callable, Optional
from .loader import CSVDataLoader
from ..config import settings

logger = logging.getLogger(__name__)

def data_producer(data_queue: multiprocessing.Queue,
                 shared_state,
                 csv_path: Optional[str] = None,
                 rate: int = settings.TICK_PROCESSING_RATE):
    """
    Producer process that reads CSV data and pushes ticks to queue.
    
    Args:
        data_queue: Multiprocessing queue to push ticks
        shared_state: Shared state object
        csv_path: Path to CSV file
        rate: Ticks per second processing rate
    """
    try:
        if csv_path is None:
            # Use sample data
            csv_path = settings.DATA_DIR / "sample_data.csv"
        
        loader = CSVDataLoader(str(csv_path))
        ticks = loader.get_ticks()
        
        logger.info(f"Producer: Starting with {len(ticks)} ticks")
        
        tick_interval = 1.0 / rate  # seconds between ticks
        
        for tick in ticks:
            data_queue.put(tick, timeout=5)
            shared_state.increment_tick_count()
            time.sleep(tick_interval)
        
        # Send stop signals
        logger.info("Producer: Finished, sending STOP signals")
        for _ in range(settings.NUM_WORKER_PROCESSES):
            data_queue.put("STOP", timeout=5)
        
        logger.info("Producer: Complete")
    
    except Exception as e:
        logger.error(f"Producer error: {str(e)}")
        raise
