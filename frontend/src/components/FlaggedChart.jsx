import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

export default function FlaggedChart({ genuineCount = 0, suspiciousCount = 0 }) {
  const data = [
    { name: 'Verified Genuine Reviews', value: genuineCount, color: '#10B981' },
    { name: 'Flagged Suspicious Reviews', value: suspiciousCount, color: '#F43F5E' },
  ];

  if (genuineCount === 0 && suspiciousCount === 0) {
    data[0].value = 1;
  }

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-card space-y-2">
      <h4 className="font-extrabold text-lg text-slate-900">Corpus Authenticity Distribution</h4>
      <p className="text-xs text-slate-500">Proportion of authentic vs flagged evidence items</p>
      
      <div className="h-64 w-full pt-2">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={55}
              outerRadius={85}
              paddingAngle={4}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ backgroundColor: '#0F172A', color: '#FFFFFF', borderRadius: '12px', border: 'none', fontSize: '12px' }}
            />
            <Legend 
              wrapperStyle={{ fontFamily: 'Inter', fontSize: '13px' }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
