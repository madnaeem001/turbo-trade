import React, { useState, useEffect } from 'react';
import FileUploader from './FileUploader';
import StrategyRanking from './StrategyRanking';
import PnLChart from './Charts/PnLChart';
import LatencyChart from './Charts/LatencyChart';
import TradeLog from './Charts/TradeLog';
import SpeedupChart from './Charts/SpeedupChart';
import Alerts from './Alerts';
import { useWebSocket } from '../hooks/useWebSocket';
import { useApi } from '../hooks/useApi';

function Dashboard({ mode, onBack, isRunning, onSimulationStart, onSimulationStop }) {
  const [fileUploaded, setFileUploaded] = useState(false);
  const [metrics, setMetrics] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [chartData, setChartData] = useState({
    pnl: [],
    latency: [],
    trades: [],
  });

  // WebSocket hook for real-time metrics
  const wsData = useWebSocket(
    process.env.REACT_APP_WS_URL,
    isRunning
  );

  // API hook
  const { startSimulation, getResults } = useApi();

  // Update metrics from WebSocket
  useEffect(() => {
    if (wsData) {
      setMetrics(wsData);
      
      // Update chart data
      if (wsData.pnl) {
        setChartData(prev => ({
          ...prev,
          pnl: [
            ...prev.pnl,
            { time: new Date().toLocaleTimeString(), ...wsData.pnl }
          ].slice(-50) // Keep last 50 points
        }));
      }
    }
  }, [wsData]);

  const handleFileSelect = async (file) => {
    // Upload file and start simulation
    setFileUploaded(true);
    onSimulationStart();

    try {
      await startSimulation({
        csv_file: file.name,
        mode: mode,
        strategies: ['sma_crossover', 'rsi_oversold', 'momentum', 'volume_spike']
      });
    } catch (error) {
      console.error('Start simulation error:', error);
      setAlerts(prev => [...prev, {
        type: 'error',
        message: 'Failed to start simulation: ' + error.message
      }]);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">
            {mode === 'OPTIMIZATION' ? 'Strategy Optimization' : 'Live Decision Support'}
          </h2>
          <p className="text-slate-400">
            {mode === 'OPTIMIZATION'
              ? 'Batch test all strategies against historical data'
              : 'Real-time trading signals from optimal strategy'
            }
          </p>
        </div>
        <button
          onClick={onBack}
          className="bg-slate-700 hover:bg-slate-600 text-white font-bold py-2 px-6 rounded-lg transition-colors"
        >
          <i className="fas fa-arrow-left mr-2"></i>Back
        </button>
      </div>

      {/* Alerts */}
      {alerts.length > 0 && <Alerts alerts={alerts} />}

      {/* File Upload / Status */}
      {!fileUploaded ? (
        <FileUploader onFileSelect={handleFileSelect} />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <p className="text-slate-400 text-sm">Status</p>
            <p className="text-2xl font-bold text-white">
              {isRunning ? <span className="text-green-400"><i className="fas fa-check-circle mr-2"></i>Running</span> : 'Completed'}
            </p>
          </div>
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <p className="text-slate-400 text-sm">Ticks Processed</p>
            <p className="text-2xl font-bold text-white">{metrics?.total_ticks || 0}</p>
          </div>
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <p className="text-slate-400 text-sm">Trades Executed</p>
            <p className="text-2xl font-bold text-white">{metrics?.trades_executed || 0}</p>
          </div>
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <p className="text-slate-400 text-sm">Avg Latency</p>
            <p className="text-2xl font-bold text-white">{metrics?.avg_latency_ms?.toFixed(2) || 0}ms</p>
          </div>
        </div>
      )}

      {/* Charts */}
      {fileUploaded && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* P&L Chart */}
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-white font-bold mb-4 text-lg">
              <i className="fas fa-chart-line text-cyan-400 mr-2"></i>
              Cumulative P&L
            </h3>
            <PnLChart data={chartData.pnl} metrics={metrics} />
          </div>

          {/* Latency Chart */}
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-white font-bold mb-4 text-lg">
              <i className="fas fa-hourglass-end text-green-400 mr-2"></i>
              Execution Latency
            </h3>
            <LatencyChart metrics={metrics} />
          </div>

          {/* Speedup Chart (Optimization Mode) */}
          {mode === 'OPTIMIZATION' && (
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <h3 className="text-white font-bold mb-4 text-lg">
                <i className="fas fa-tachometer-alt text-orange-400 mr-2"></i>
                Parallel vs Serial Speedup
              </h3>
              <SpeedupChart metrics={metrics} />
            </div>
          )}

          {/* Strategy Ranking (Optimization Mode) */}
          {mode === 'OPTIMIZATION' && (
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <h3 className="text-white font-bold mb-4 text-lg">
                <i className="fas fa-trophy text-yellow-400 mr-2"></i>
                Strategy Rankings
              </h3>
              <StrategyRanking metrics={metrics} />
            </div>
          )}
        </div>
      )}

      {/* Trade Log */}
      {fileUploaded && (
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-white font-bold mb-4 text-lg">
            <i className="fas fa-exchange-alt text-purple-400 mr-2"></i>
            Recent Trades
          </h3>
          <TradeLog trades={metrics?.trades || []} />
        </div>
      )}

      {/* Action Buttons */}
      {fileUploaded && (
        <div className="flex gap-4 justify-center">
          {isRunning ? (
            <button
              onClick={onSimulationStop}
              className="bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-8 rounded-lg transition-colors"
            >
              <i className="fas fa-stop-circle mr-2"></i>Stop Simulation
            </button>
          ) : (
            <button
              onClick={onBack}
              className="bg-slate-700 hover:bg-slate-600 text-white font-bold py-3 px-8 rounded-lg transition-colors"
            >
              <i className="fas fa-times mr-2"></i>Close
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default Dashboard;