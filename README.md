# TurboTrade — Parallel HFT Backtesting Engine

> A high-performance, multi-process trading engine that runs four quantitative strategies concurrently against historical or live market data, with a real-time React dashboard for monitoring, analysis, and decision support.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Tech Stack](#tech-stack)
5. [Project Structure](#project-structure)
6. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Backend Setup](#backend-setup)
   - [Frontend Setup](#frontend-setup)
   - [Running the Project](#running-the-project)
7. [Operating Modes](#operating-modes)
8. [Trading Strategies](#trading-strategies)
9. [Core Engine](#core-engine)
10. [API Reference](#api-reference)
11. [WebSocket Protocol](#websocket-protocol)
12. [Configuration](#configuration)
13. [Data Format](#data-format)
14. [Testing](#testing)
15. [Performance](#performance)

---

## Overview

TurboTrade is a **parallel and distributed computing** project that simulates a High-Frequency Trading (HFT) backtesting engine. It demonstrates how multiple trading strategies can be evaluated simultaneously using Python's `multiprocessing` module, with all order execution flowing through a thread-safe Order Matching Engine (OME).

The system has two modes:

| Mode | Description |
|------|-------------|
| **Optimization** | Batch-test all four strategies against historical CSV data and rank them by final P&L |
| **Live Decision Support** | Stream market data through the best strategy and receive real-time BUY/SELL signals |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        React Frontend                           │
│  ModeSelector → Dashboard → Charts / TradeLog / StrategyRanking │
│              WebSocket (ws://localhost:8000/ws)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP / WebSocket
┌────────────────────────────▼────────────────────────────────────┐
│                  FastAPI Backend (port 8000)                     │
│  /api/upload  /api/start  /api/results  /api/health  /ws        │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     Execution Engine                            │
│                                                                 │
│  ┌──────────────┐    ┌─────────────────────┐                   │
│  │ Data Producer│    │ Strategy Workers (N) │                   │
│  │  (Process)   │───▶│  SMA / RSI /         │                   │
│  └──────────────┘    │  Momentum / Volume   │                   │
│   CSV / Live Feed    └──────────┬───────────┘                   │
│                                 │ Orders                         │
│  ┌──────────────────────────────▼───────────┐                   │
│  │       Order Matching Engine (OME)        │                   │
│  │  Price-Time Priority  •  FIFO Matching   │                   │
│  └──────────────────────────────┬───────────┘                   │
│                                 │ Trades                         │
│  ┌──────────────────────────────▼───────────┐                   │
│  │         Shared State (Manager)           │                   │
│  │  PnL Dict  •  Trade Log  •  Latency List │                   │
│  └──────────────────────────────────────────┘                   │
│  ┌─────────────────────────────────────────┐                    │
│  │       Concurrency Controller            │                    │
│  │  PnL Lock  •  Trade Lock  •  State Lock │                    │
│  └─────────────────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Features

### Backend

- **Parallel Strategy Execution** — Up to 4 strategy worker processes run simultaneously using `ProcessPoolExecutor`, each consuming the same market tick queue independently.
- **Order Matching Engine (OME)** — Deterministic order matching with FIFO price-time priority. All orders from all strategies compete on the same order book.
- **Shared State Management** — Cross-process shared dictionaries and lists via `multiprocessing.Manager()` to safely accumulate P&L, trade logs, and latency measurements.
- **Concurrency Controller** — Dedicated `multiprocessing.Lock` objects for P&L updates, trade logging, and latency recording, preventing race conditions.
- **Data Producer Process** — Dedicated process that reads CSV market data and pushes tick-by-tick data into a bounded queue at a configurable rate (default 1,000 ticks/second).
- **CSV Data Loader** — Reads standard OHLCV CSV files:  `timestamp, open, high, low, close, volume`.
- **Sample Data Generator** — Generates 25,200 minutes of realistic synthetic OHLCV data using geometric Brownian motion for testing without real market data.
- **Real-Time WebSocket Streaming** — Broadcasts live metrics (P&L, latency, tick count, trade count) to all connected clients every 100ms.
- **REST API** — FastAPI endpoints for uploading data files, starting a simulation, fetching results, and health-checking.
- **Redis Integration** — Optional Redis backend for persistent state sharing across distributed nodes.
- **Structured Logging** — JSON-formatted log output with configurable log levels, written to `backend/logs/`.
- **Pytest Test Suite** — Unit tests for the OME, shared state, and individual strategies, plus an integration test for a full end-to-end simulation run.

### Frontend

- **Mode Selector** — Landing screen to choose between Optimization or Live Decision Support modes.
- **Dashboard** — Central hub displaying all real-time metrics and charts after a simulation starts.
- **File Uploader** — Drag-and-drop (or click-to-browse) CSV upload interface that triggers the backend simulation.
- **P&L Chart** — Line chart tracking cumulative profit/loss per strategy over time (rolling 50-point window).
- **Latency Chart** — Visualizes order execution latency in milliseconds across the simulation run.
- **Speedup Chart** *(Optimization Mode only)* — Bar chart comparing parallel vs. serial execution throughput.
- **Trade Log** — Scrollable live log of executed trades with symbol, side, quantity, price, and P&L.
- **Strategy Ranking** — Live leaderboard sorted by total P&L: SMA Crossover, RSI Oversold, Momentum, Volume Spike.
- **Alerts Panel** — Inline error/success/info notifications for upload failures, simulation state changes, and WebSocket disconnects.
- **Status Indicators** — Animated spinner in the header and status cards showing ticks processed, trades executed, and average latency.
- **Tailwind CSS Theming** — Dark slate UI with cyan/green accent colors, fully responsive grid layout.
- **Real-Time WebSocket Hook** — `useWebSocket` custom React hook that automatically reconnects and feeds live data to all chart components.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI 0.109, Uvicorn 0.27 |
| Strategy Engine | Python 3.x, `multiprocessing`, `concurrent.futures` |
| Data Processing | Pandas 2.x, NumPy 1.26, SciPy |
| State Sharing | `multiprocessing.Manager`, Redis 5.x |
| WebSockets | FastAPI WebSocket, `python-socketio` |
| Frontend | React 18, React Router 6 |
| Charts | Chart.js 4, `react-chartjs-2`, Recharts |
| Styling | Tailwind CSS 3, PostCSS |
| HTTP Client | Axios |
| Testing | Pytest 7, `pytest-asyncio`, `pytest-benchmark`, HTTPX |
| Config | Pydantic Settings 2, `python-dotenv` |

---

## Project Structure

```
HFT PROJECT/
├── README.md
├── backend/
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── src/
│   │   ├── config.py               # Global Pydantic settings (env vars, ports, limits)
│   │   ├── main.py                 # CLI entry point — runs parallel simulation directly
│   │   ├── api/
│   │   │   ├── server.py           # FastAPI app, CORS, startup/shutdown lifecycle
│   │   │   ├── routes.py           # REST endpoints: /upload, /start, /results, /health
│   │   │   ├── websocket.py        # WebSocketManager + websocket_handler
│   │   │   └── models.py           # Pydantic request/response models
│   │   ├── core/
│   │   │   ├── engine.py           # ExecutionEngine — orchestrates all processes
│   │   │   ├── ome.py              # OrderMatchingEngine — FIFO price-time matching
│   │   │   ├── shared_state.py     # SharedState — cross-process Manager dicts/lists
│   │   │   └── locks.py            # ConcurrencyController — multiprocessing Locks
│   │   ├── strategies/
│   │   │   ├── base_strategy.py    # BaseStrategy ABC + indicator calculations
│   │   │   ├── sma_strategy.py     # SMA crossover (fast/slow period)
│   │   │   ├── rsi_strategy.py     # RSI oversold/overbought
│   │   │   ├── momentum_strategy.py# Price momentum threshold crossover
│   │   │   └── volume_strategy.py  # Volume spike + price direction
│   │   └── data/
│   │       ├── loader.py           # CSVDataLoader — reads OHLCV CSV files
│   │       ├── producer.py         # data_producer — tick queue feeder process
│   │       ├── sample_data.csv     # Pre-generated 25k-row OHLCV dataset
│   │       ├── sample_data_generator.py  # Synthetic data generator script
│   │       └── uploads/            # Uploaded CSV files from frontend
│   ├── tests/
│   │   ├── test_core.py            # OME, SharedState, SMAStrategy, RSIStrategy unit tests
│   │   └── test_integration.py     # Full simulation integration test
│   ├── logs/                       # Runtime log files
│   └── venv/                       # Python virtual environment
└── frontend/
    ├── package.json
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── public/
    │   └── index.html
    └── src/
        ├── App.jsx                 # Root component — header, mode routing, footer
        ├── components/
        │   ├── ModeSelector.jsx    # Landing mode selection cards
        │   ├── Dashboard.jsx       # Main dashboard with metrics, charts, uploads
        │   ├── FileUploader.jsx    # CSV drag-and-drop upload component
        │   ├── StrategyRanking.jsx # Live P&L leaderboard
        │   ├── Alerts.jsx          # Error/success/info notification panel
        │   └── Charts/
        │       ├── PnLChart.jsx    # Cumulative P&L line chart
        │       ├── LatencyChart.jsx# Execution latency chart
        │       ├── TradeLog.jsx    # Scrollable executed trades table
        │       └── SpeedupChart.jsx# Parallel vs serial speedup bar chart
        ├── hooks/
        │   ├── useWebSocket.js     # Auto-reconnecting WebSocket hook
        │   └── useApi.js           # Axios API calls hook
        └── services/               # API service layer
```

---

## Getting Started

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| Node.js | 18+ |
| npm | 9+ |
| Redis | 6+ |

Make sure Redis is running before starting the backend:

```bash
# macOS (Homebrew)
brew services start redis

# Linux
sudo systemctl start redis

# Verify
redis-cli ping   # Should return: PONG
```

---

### Backend Setup

```bash
cd "HFT PROJECT/backend"

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

**Optional:** Generate fresh sample data (25,200 rows) if `sample_data.csv` is missing:

```bash
python data/sample_data_generator.py
```

---

### Frontend Setup

```bash
cd "HFT PROJECT/frontend"

# Install Node dependencies
npm install
```

**Optional:** Create a `.env` file in `frontend/` to configure the API URLs:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

---

### Running the Project

**Terminal 1 — Start the backend API server:**

```bash
cd "HFT PROJECT/backend"
source venv/bin/activate
uvicorn src.api.server:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`  
Interactive API docs (Swagger UI): `http://localhost:8000/docs`

**Terminal 2 — Start the React frontend:**

```bash
cd "HFT PROJECT/frontend"
npm start
```

The UI will open at: `http://localhost:3000`

**Alternative — Run CLI simulation directly (no API):**

```bash
cd "HFT PROJECT/backend"
source venv/bin/activate
python -m src.main
```

---

## Operating Modes

### Optimization Mode

Designed for backtesting and strategy comparison against historical data.

1. Select **Optimization Mode** from the landing screen.
2. Upload a CSV file with OHLCV market data (or use the built-in sample data).
3. The engine spawns 4 parallel strategy worker processes.
4. All four strategies process the same tick stream simultaneously.
5. Results show final P&L rankings, trade logs, latency measurements, and parallel vs. serial speedup.

### Live Decision Support Mode

Designed for real-time signal generation.

1. Select **Live Decision Support** from the landing screen.
2. Upload a CSV file to simulate a live feed (tick-by-tick replay at 1,000 ticks/second).
3. The engine runs the best-performing strategy and emits BUY/SELL signals via WebSocket.
4. The dashboard shows real-time P&L, latency, and instant trade alerts.

---

## Trading Strategies

All strategies extend the `BaseStrategy` abstract class and implement a single `evaluate(tick)` method that returns an order dict or `None`.

### 1. SMA Crossover (`SMAStrategy`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `fast_period` | 5 | Period for fast moving average |
| `slow_period` | 20 | Period for slow moving average |

- **BUY** when the fast SMA crosses above the slow SMA (bullish crossover).
- **SELL** when the fast SMA crosses below the slow SMA (bearish crossover).
- Signals only fire on the actual crossover tick, not when already above/below.

### 2. RSI Oversold/Overbought (`RSIStrategy`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `period` | 14 | RSI lookback window |
| `oversold` | 30 | RSI threshold for BUY signal |
| `overbought` | 70 | RSI threshold for SELL signal |

- **BUY** when RSI drops below 30 (market is oversold).
- **SELL** when RSI rises above 70 (market is overbought).
- Prevents duplicate signals — only fires on state transitions.

### 3. Price Momentum (`MomentumStrategy`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `period` | 10 | Lookback period for momentum calculation |
| `threshold` | 0 | Zero-line or custom threshold |

- **BUY** when momentum crosses up through the threshold (from negative/zero to positive).
- **SELL** when momentum crosses down through the threshold (from positive to negative/zero).
- Momentum is calculated as: `current_price − price_N_ticks_ago`.

### 4. Volume Spike (`VolumeStrategy`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `window` | 20 | Rolling window for average volume |
| `multiplier` | 1.5 | Volume must exceed `avg × multiplier` to signal |

- Detects unusual trading activity when current volume exceeds 1.5× the rolling average.
- **BUY** when volume spike accompanies an upward price move.
- **SELL** when volume spike accompanies a downward price move.

### Built-In Indicators (available in `BaseStrategy`)

| Indicator | Method |
|-----------|--------|
| Simple Moving Average | `calculate_sma(period)` |
| Exponential Moving Average | `calculate_ema(period)` |
| Relative Strength Index | `calculate_rsi(period)` |
| Price Momentum | `calculate_momentum(period)` |
| Bollinger Bands | `calculate_bollinger_bands(period, std_dev)` |

---

## Core Engine

### ExecutionEngine

The central orchestrator in `src/core/engine.py`.

- Creates and manages `SharedState`, `ConcurrencyController`, `OrderMatchingEngine`, and the data queue.
- `run_simulation()` — launches a `ProcessPoolExecutor` with one data producer and N strategy workers.
- `process_order()` — thread-safe order submission and matching, must be called within a lock context.
- `get_results()` — returns final summary: status, P&L per strategy, avg latency, total ticks, total trades, execution time, and the last 100 executed trades.
- `get_live_metrics()` — returns a lightweight snapshot for WebSocket broadcasts.

### Order Matching Engine (OME)

Implemented in `src/core/ome.py`.

- Maintains a price-sorted order book split into `BUY` and `SELL` sides.
- Matching algorithm: **price-time priority** — highest bid vs. lowest ask; ties broken by order arrival time.
- Executes at the **sell-side price** (sell price priority).
- Tracks `Order` and `Trade` dataclasses including: order ID, strategy ID, symbol, side, quantity, price, execution price, P&L, timestamp, and latency in milliseconds.

### SharedState

Implemented in `src/core/shared_state.py`.

- Uses `multiprocessing.Manager()` to create proxy objects accessible across process boundaries.
- Stores: strategy P&L dictionary, list of all latency measurements, trade log, and overall status.
- Key methods: `update_pnl()`, `add_trade()`, `add_latency()`, `increment_tick_count()`, `get_snapshot()`.

### ConcurrencyController

Implemented in `src/core/locks.py`.

Provides four independent `multiprocessing.Lock` objects:

| Lock | Protects |
|------|----------|
| `pnl_lock` | P&L dictionary updates |
| `trade_log_lock` | Trade log appends |
| `latency_lock` | Latency list appends |
| `state_lock` | General state mutations |

---

## API Reference

Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Service info and status |
| `GET` | `/api/health` | Health check — returns `{"status": "healthy"}` |
| `POST` | `/api/upload` | Upload a CSV market data file (multipart/form-data) |
| `POST` | `/api/start` | Start an optimization or live simulation |
| `GET` | `/api/results` | Fetch final simulation results |
| `WS` | `/ws` | WebSocket connection for real-time metric streaming |

### POST /api/upload

```json
// Response
{
  "filename": "market_data.csv",
  "size": 1048576,
  "status": "success"
}
```

### POST /api/start

```json
// Request body
{
  "csv_file": "market_data.csv",
  "mode": "OPTIMIZATION",
  "strategies": ["sma_crossover", "rsi_oversold", "momentum", "volume_spike"],
  "duration_seconds": null
}

// Response
{
  "status": "simulation_started",
  "mode": "OPTIMIZATION",
  "strategies": ["sma_crossover", "rsi_oversold", "momentum", "volume_spike"]
}
```

### GET /api/results

```json
{
  "status": "COMPLETED",
  "pnl": {
    "S1": 1250.50,
    "S2": 800.25,
    "S3": -150.00,
    "S4": 2100.75
  },
  "avg_latency_ms": 0.42,
  "total_ticks": 25200,
  "total_trades": 312,
  "execution_time_sec": 25.8,
  "trades": [ ... ]
}
```

Full interactive documentation is available at `http://localhost:8000/docs` (Swagger UI).

---

## WebSocket Protocol

Connect to `ws://localhost:8000/ws`.

The server broadcasts JSON messages every **100ms** while a simulation is running:

### Metrics Message

```json
{
  "type": "metrics",
  "data": {
    "status": "RUNNING",
    "pnl": { "S1": 100.5, "S2": 75.0, "S3": -20.0, "S4": 200.0 },
    "avg_latency": 0.35,
    "total_ticks": 5000,
    "trade_count": 42,
    "timestamp": "2026-03-09T02:00:00.000Z"
  }
}
```

### Trade Message

```json
{
  "type": "trade",
  "data": {
    "trade_id": "TRD-42",
    "strategy_id": "S4",
    "symbol": "AAPL",
    "side": "BUY",
    "quantity": 10,
    "price": 152.40,
    "execution_price": 152.40,
    "pnl": 12.50,
    "latency_ms": 0.28
  }
}
```

---

## Configuration

All settings live in `backend/src/config.py` and can be overridden with environment variables or a `.env` file placed in the `backend/` directory.

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Runtime environment |
| `NUM_WORKER_PROCESSES` | `4` | Parallel strategy workers |
| `TICK_PROCESSING_RATE` | `1000` | Ticks per second |
| `MAX_QUEUE_SIZE` | `10000` | Bounded queue capacity |
| `USE_REDIS` | `True` | Enable Redis state backend |
| `REDIS_HOST` | `localhost` | Redis server hostname |
| `REDIS_PORT` | `6379` | Redis server port |
| `SERVER_PORT` | `8000` | FastAPI server port |
| `UVICORN_WORKERS` | `4` | Uvicorn worker processes |
| `CORS_ORIGINS` | `["*"]` | Allowed CORS origins |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `MAX_UPLOAD_SIZE` | `104857600` | 100 MB max upload |
| `WS_HEARTBEAT_INTERVAL` | `0.5` | WebSocket ping interval (seconds) |
| `MAX_STRATEGIES` | `10` | Maximum concurrent strategies |

**Example `.env` file:**

```env
NUM_WORKER_PROCESSES=8
TICK_PROCESSING_RATE=5000
REDIS_HOST=localhost
REDIS_PASSWORD=mysecretpassword
LOG_LEVEL=DEBUG
```

---

## Data Format

The engine accepts any CSV file with at minimum a `close` and `volume` column. Full OHLCV format is recommended:

```csv
datetime,open,high,low,close,volume
2023-01-01 09:30:00,99.82,100.54,99.10,100.12,5423
2023-01-01 09:31:00,100.12,100.87,99.95,100.65,3871
...
```

| Column | Required | Description |
|--------|----------|-------------|
| `datetime` | No | ISO timestamp (used as index) |
| `open` | No | Opening price |
| `high` | No | Period high |
| `low` | No | Period low |
| `close` | **Yes** | Closing price (used as tick price) |
| `volume` | **Yes** | Traded volume |

To generate a synthetic 25,200-row test dataset:

```bash
cd backend
source venv/bin/activate
python data/sample_data_generator.py
```

---

## Testing

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html to view coverage

# Run benchmarks
pytest --benchmark-only
```

### Test Coverage

| Test File | Coverage |
|-----------|----------|
| `test_core.py` | SharedState init, P&L updates, OME order submission, OME order matching, SMA strategy, RSI strategy |
| `test_integration.py` | Full parallel simulation end-to-end with mock data producer and worker |

---

## Performance

The engine is designed to demonstrate **parallel speedup** against a serial baseline:

- **Serial baseline** — All four strategies process ticks sequentially in a single process.
- **Parallel execution** — All four strategies run as separate OS processes with independent CPU cores.

Expected speedup with 4 workers on a 4-core machine: **~3–3.8×** for compute-bound strategy logic.

Latency measurements record the time from tick arrival to trade execution at sub-millisecond precision, exposed via the `/api/results` endpoint and the latency WebSocket broadcast.

Key performance levers in `config.py`:

```python
TICK_PROCESSING_RATE = 1000   # Increase for faster throughput testing
NUM_WORKER_PROCESSES = 4      # Set to CPU core count for max speedup
MAX_QUEUE_SIZE = 10000        # Tune based on available memory
```

---

## License

This project was developed as a Parallel & Distributed Computing coursework demonstration.
