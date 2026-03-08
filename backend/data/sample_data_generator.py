import pandas as pd
import numpy as np
from pathlib import Path

def generate_sample_data(filepath, days=252, initial_price=100):
    """Generate realistic OHLCV data for testing"""
    
    # Generate price path
    dates = pd.date_range(start='2023-01-01', periods=days*100, freq='1min')
    returns = np.random.normal(0.0001, 0.002, len(dates))
    prices = initial_price * np.exp(np.cumsum(returns))
    
    data = {
        'datetime': dates,
        'open': prices + np.random.uniform(-0.5, 0.5, len(prices)),
        'high': prices + np.random.uniform(0, 1, len(prices)),
        'low': prices + np.random.uniform(-1, 0, len(prices)),
        'close': prices,
        'volume': np.random.uniform(1000, 10000, len(prices)).astype(int)
    }
    
    df = pd.DataFrame(data)
    df.set_index('datetime', inplace=True)
    df.to_csv(filepath)
    print(f"Generated {len(df)} ticks to {filepath}")

if __name__ == "__main__":
    output_path = Path(__file__).parent / "sample_data.csv"
    generate_sample_data(str(output_path))
