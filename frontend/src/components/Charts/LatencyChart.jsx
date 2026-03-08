import React from 'react';

function LatencyChart({ metrics }) {
  const latency = metrics?.avg_latency_ms || 0;

  return (
    <div className="flex flex-col items-center justify-center h-300 space-y-6">
      <div className="text-6xl font-bold text-cyan-400">
        {latency.toFixed(2)}
        <span className="text-2xl ml-2">ms</span>
      </div>
      <div className="w-full bg-slate-700 rounded-full h-3 overflow-hidden">
        <div
          className="bg-gradient-to-r from-cyan-500 to-green-500 h-full transition-all"
          style={{
            width: `${Math.min((latency / 100) * 100, 100)}%`
          }}
        ></div>
      </div>
      <p className="text-slate-400 text-center text-sm">
        Ultra-low latency order execution time
      </p>
      <div className="grid grid-cols-3 gap-4 w-full pt-4">
        <div className="bg-slate-700/50 rounded p-3 text-center">
          <p className="text-xs text-slate-400">Min</p>
          <p className="text-sm font-bold text-white">~5ms</p>
        </div>
        <div className="bg-slate-700/50 rounded p-3 text-center">
          <p className="text-xs text-slate-400">Avg</p>
          <p className="text-sm font-bold text-white">{latency.toFixed(1)}ms</p>
        </div>
        <div className="bg-slate-700/50 rounded p-3 text-center">
          <p className="text-xs text-slate-400">Max</p>
          <p className="text-sm font-bold text-white">~50ms</p>
        </div>
      </div>
    </div>
  );
}

export default LatencyChart;