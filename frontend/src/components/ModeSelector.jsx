import React from 'react';

function ModeSelector({ onModeSelect }) {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-white mb-4">
          Select Operating Mode
        </h2>
        <p className="text-slate-300 text-lg">
          Choose between optimizing strategies or running in real-time decision support mode
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Optimization Mode */}
        <div
          onClick={() => onModeSelect('OPTIMIZATION')}
          className="group cursor-pointer bg-gradient-to-br from-slate-800 to-slate-900 border-2 border-slate-700 hover:border-cyan-500 rounded-xl p-8 transition-all duration-300 hover:shadow-2xl hover:shadow-cyan-500/20 transform hover:scale-105"
        >
          <div className="text-5xl mb-4 text-cyan-400 group-hover:scale-110 transition-transform">
            <i className="fas fa-chart-line"></i>
          </div>
          <h3 className="text-2xl font-bold text-white mb-3">Optimization Mode</h3>
          <p className="text-slate-300 mb-6">
            Upload historical CSV data and run all strategies in parallel to find optimal parameters. Get comprehensive rankings and P&L analysis.
          </p>
          <ul className="space-y-2 text-slate-400 text-sm mb-6">
            <li><i className="fas fa-check text-green-400 mr-2"></i>Batch process historical data</li>
            <li><i className="fas fa-check text-green-400 mr-2"></i>Run 4 strategies in parallel</li>
            <li><i className="fas fa-check text-green-400 mr-2"></i>Get final P&L rankings</li>
            <li><i className="fas fa-check text-green-400 mr-2"></i>Measure speedup metrics</li>
          </ul>
          <button className="w-full bg-gradient-to-r from-cyan-500 to-cyan-600 hover:from-cyan-600 hover:to-cyan-700 text-white font-bold py-3 px-6 rounded-lg transition-all">
            Launch <i className="fas fa-arrow-right ml-2"></i>
          </button>
        </div>

        {/* Live Mode */}
        <div
          onClick={() => onModeSelect('LIVE')}
          className="group cursor-pointer bg-gradient-to-br from-slate-800 to-slate-900 border-2 border-slate-700 hover:border-green-500 rounded-xl p-8 transition-all duration-300 hover:shadow-2xl hover:shadow-green-500/20 transform hover:scale-105"
        >
          <div className="text-5xl mb-4 text-green-400 group-hover:scale-110 transition-transform">
            <i className="fas fa-tower-broadcast"></i>
          </div>
          <h3 className="text-2xl font-bold text-white mb-3">Live Decision Support</h3>
          <p className="text-slate-300 mb-6">
            Run optimal strategy on live market data. Get real-time BUY/SELL signals with execution latency metrics.
          </p>
          <ul className="space-y-2 text-slate-400 text-sm mb-6">
            <li><i className="fas fa-check text-green-400 mr-2"></i>Real-time market data feed</li>
            <li><i className="fas fa-check text-green-400 mr-2"></i>Instant buy/sell alerts</li>
            <li><i className="fas fa-check text-green-400 mr-2"></i>Ultra-low latency metrics</li>
            <li><i className="fas fa-check text-green-400 mr-2"></i>Live P&L tracking</li>
          </ul>
          <button className="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-bold py-3 px-6 rounded-lg transition-all">
            Launch <i className="fas fa-arrow-right ml-2"></i>
          </button>
        </div>
      </div>

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
          <div className="text-3xl text-cyan-400 mb-3"><i className="fas fa-microchip"></i></div>
          <h4 className="text-white font-bold mb-2">4 Parallel Processes</h4>
          <p className="text-slate-400 text-sm">Strategies S1, S2, S3, S4 running concurrently for maximum speedup</p>
        </div>
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
          <div className="text-3xl text-green-400 mb-3"><i className="fas fa-bolt"></i></div>
          <h4 className="text-white font-bold mb-2">Atomic Execution</h4>
          <p className="text-slate-400 text-sm">Order Matching Engine ensures deterministic, conflict-free order resolution</p>
        </div>
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
          <div className="text-3xl text-orange-400 mb-3"><i className="fas fa-gauge-high"></i></div>
          <h4 className="text-white font-bold mb-2">Real-time Metrics</h4>
          <p className="text-slate-400 text-sm">P&L, latency, and trade logs streamed via WebSocket</p>
        </div>
      </div>
    </div>
  );
}

export default ModeSelector;