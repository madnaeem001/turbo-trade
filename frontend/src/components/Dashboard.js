import React, { useState } from 'react';
import '../styles/Dashboard.css';

function Dashboard({ mode, onChangeMode }) {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setLoading(true);
      setTimeout(() => {
        setLoading(false);
        setResults({
          strategies: [
            { name: 'SMA Crossover', pnl: 1234.56, trades: 45 },
            { name: 'RSI Oversold', pnl: 2456.78, trades: 52 },
            { name: 'Momentum', pnl: 987.65, trades: 38 },
            { name: 'Volume Spike', pnl: 1890.45, trades: 48 }
          ],
          speedup: '3.37x'
        });
      }, 2000);
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>{mode === 'optimization' ? '📊 Optimization Mode' : '📈 Live Mode'}</h2>
        <button className="back-btn" onClick={onChangeMode}>← Back</button>
      </div>

      <div className="upload-section">
        <h3>Upload Market Data (CSV)</h3>
        <input 
          type="file" 
          accept=".csv" 
          onChange={handleUpload}
          disabled={loading}
        />
        {loading && <p className="loading">Processing... ⏳</p>}
      </div>

      {results && (
        <div className="results-section">
          <h3>Strategy Results</h3>
          <div className="metrics">
            <div className="metric-card">
              <h4>Speedup Factor</h4>
              <p className="metric-value">{results.speedup}</p>
            </div>
          </div>

          <table className="results-table">
            <thead>
              <tr>
                <th>Strategy</th>
                <th>P&L ($)</th>
                <th>Trades</th>
              </tr>
            </thead>
            <tbody>
              {results.strategies.map((s, i) => (
                <tr key={i}>
                  <td>{s.name}</td>
                  <td className={s.pnl > 0 ? 'positive' : 'negative'}>
                    ${s.pnl.toFixed(2)}
                  </td>
                  <td>{s.trades}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
