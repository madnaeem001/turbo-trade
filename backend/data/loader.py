import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class CSVDataLoader:
    """Load and parse CSV data files in OHLCV format"""
    
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        self.df: Optional[pd.DataFrame] = None
    
    def load(self) -> pd.DataFrame:
        """Load CSV file into DataFrame"""
        try:
            # Expected columns: timestamp, open, high, low, close, volume
            self.df = pd.read_csv(self.filepath)
            
            # Validate required columns
            required = {"close", "volume"}  # Minimal required
            if not required.issubset(set(self.df.columns)):
                raise ValueError(f"CSV missing required columns: {required}")
            
            # Ensure numeric types
            for col in ["close", "volume"]:
                if col in self.df.columns:
                    self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
            
            logger.info(f"Loaded {len(self.df)} rows from {self.filepath.name}")
            return self.df
        
        except Exception as e:
            logger.error(f"Error loading CSV: {str(e)}")
            raise
    
    def get_ticks(self) -> List[Dict[str, Any]]:
        """Convert DataFrame to tick list"""
        if self.df is None:
            self.load()
        
        ticks = []
        for idx, row in self.df.iterrows():
            tick = {
                "timestamp": idx,
                "price": row.get("close", 0),
                "volume": row.get("volume", 0),
                "open": row.get("open", row.get("close", 0)),
                "high": row.get("high", row.get("close", 0)),
                "low": row.get("low", row.get("close", 0)),
            }
            ticks.append(tick)
        
        return ticks
    
    def get_random_sample(self, n: int = 100) -> List[Dict[str, Any]]:
        """Get random sample of ticks"""
        if self.df is None:
            self.load()
        sample_df = self.df.sample(n=min(n, len(self.df)))
        return self.get_ticks()  # Simplified version
