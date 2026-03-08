import React from 'react';

function StrategyRanking({ metrics }) {
  const strategies = [
    { id: 'S1', name: 'SMA Crossover (5/20)', icon: 'fa-line-chart' },
    { id: 'S2', name: 'RSI Oversold', icon: 'fa-chart-area' },
    { id: 'S3', name: 'Momentum', icon: 'fa-arrow-trend-up' },
    { id: 'S4', name: 'Volume Spike', icon: 'fa-wave-square' },
  ];

  const pnl = metrics?.pnl || {};
  
  const ranked = strategies
    .map(s => ({ ...s, profit: pnl[s.id] || 0 }))
    .sort((a, b) => b.profit - a.profit);

  return (
    <div className="space-y-3">
      {ranked.map((strategy, index) => (
        <div
          key={strategy.id}
          className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition-colors"
        >
          <div className="flex items-center space-x-4 flex-1">
            <div className="text-2xl font-bold w-8 h-8 flex items-center justify-center bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full text-white">
              {index + 1}
            </div>
            <div>
              <p className="text-white font-semibold">{strategy.name}</p>
              <p className="text-slate-400 text-sm">{strategy.id}</p>
            </div>
          </div>
          <div className="text-right">
            <p className={`text-lg font-bold ${strategy.profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              ${strategy.profit.toFixed(2)}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}

export default StrategyRanking;
