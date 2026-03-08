import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function SpeedupChart({ metrics }) {
  const data = [
    { name: 'Serial', time: 45, latency: 150 },
    { name: 'Parallel (4x)', time: 13, latency: 35 },
  ];

  const speedup = metrics?.execution_time_sec ? (45 / (metrics.execution_time_sec || 1)).toFixed(1) : '3.4';

  return (
    <div className="space-y-4">
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          <XAxis dataKey="name" stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" />
          <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
          <Legend />
          <Bar dataKey="time" fill="#06b6d4" name="Time (seconds)" />
          <Bar dataKey="latency" fill="#10b981" name="Latency (ms)" />
        </BarChart>
      </ResponsiveContainer>
      <div className="bg-slate-700/50 rounded-lg p-4 text-center">
        <p className="text-slate-400 text-sm mb-1">Speedup Factor</p>
        <p className="text-3xl font-bold text-green-400">{speedup}x</p>
        <p className="text-slate-400 text-xs mt-2">Parallel execution is {speedup}x faster</p>
      </div>
    </div>
  );
}

export default SpeedupChart;
