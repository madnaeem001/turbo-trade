import React from 'react';

function Alerts({ alerts }) {
  return (
    <div className="space-y-3">
      {alerts.map((alert, idx) => (
        <div
          key={idx}
          className={`p-4 rounded-lg flex items-center space-x-3 ${
            alert.type === 'error'
              ? 'bg-red-500/20 border border-red-500/50 text-red-200'
              : alert.type === 'success'
              ? 'bg-green-500/20 border border-green-500/50 text-green-200'
              : 'bg-blue-500/20 border border-blue-500/50 text-blue-200'
          }`}
        >
          <i className={`fas ${
            alert.type === 'error' ? 'fa-exclamation-circle' :
            alert.type === 'success' ? 'fa-check-circle' :
            'fa-info-circle'
          }`}></i>
          <p>{alert.message}</p>
        </div>
      ))}
    </div>
  );
}

export default Alerts;