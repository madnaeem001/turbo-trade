import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function PnLChart({ data, metrics }) {
  const chartData = data.length > 0 ? data : [
    { time: 'No data', S1: 0, S2: 0, S3: 0, S4: 0 }
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
        <XAxis dataKey="time" stroke="#94a3b8" />
        <YAxis stroke="#94a3b8" />
        <Tooltip 
          contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
          labelStyle={{ color: '#fff' }}
        />
        <Legend />
        <Line type="monotone" dataKey="S1" stroke="#06b6d4" name="SMA" />
        <Line type="monotone" dataKey="S2" stroke="#10b981" name="RSI" />
        <Line type="monotone" dataKey="S3" stroke="#f59e0b" name="Momentum" />
        <Line type="monotone" dataKey="S4" stroke="#8b5cf6" name="Volume" />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default PnLChart;
