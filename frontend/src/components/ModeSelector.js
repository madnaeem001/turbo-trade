import React from 'react';
import '../styles/ModeSelector.css';

function ModeSelector({ onSelectMode }) {
  return (
    <div className="mode-selector">
      <div className="mode-card" onClick={() => onSelectMode('optimization')}>
        <h2>📊 Optimization Mode</h2>
        <p>Backtest strategies against historical data</p>
        <button>Start Optimization</button>
      </div>
      
      <div className="mode-card" onClick={() => onSelectMode('live')}>
        <h2>📈 Live Mode</h2>
        <p>Real-time trading signals and execution</p>
        <button>Start Live Trading</button>
      </div>
    </div>
  );
}

export default ModeSelector;
