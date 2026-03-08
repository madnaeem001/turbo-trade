import React from 'react';

function TradeLog({ trades }) {
  return (
    <div className="space-y-3 max-h-96 overflow-y-auto">
      {trades && trades.length > 0 ? (
        trades.slice(-20).reverse().map((trade, idx) => (
          <div key={idx} className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg text-sm">
            <div className="flex-1">
              <p className="text-white font-semibold">{trade.strategy_id}</p>
              <p className="text-slate-400 text-xs">{trade.trade_id}</p>
            </div>
            <div className="flex items-center space-x-4">
              <span className={`font-bold ${trade.side === 'BUY' ? 'text-green-400' : 'text-red-400'}`}>
                {trade.side}
              </span>
              <span className="text-slate-300">{trade.quantity} @ ${trade.execution_price.toFixed(2)}</span>
              <span className={`font-bold ${trade.pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                ${trade.pnl.toFixed(2)}
              </span>
            </div>
          </div>
        ))
      ) : (
        <p className="text-slate-400 text-center py-8">No trades yet...</p>
      )}
    </div>
  );
}

export default TradeLog;
