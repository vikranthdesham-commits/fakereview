import React from 'react';
import { Cpu, Zap, Award } from 'lucide-react';

export default function ModelAblationCard({ evaluations = [] }) {
  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-card space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-100">
        <div>
          <h3 className="font-extrabold text-xl text-slate-900 flex items-center gap-2">
            <Cpu className="w-5 h-5 text-indigo-600" /> Model Performance & Ablation Study
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Baseline TF-IDF + Logistic Regression vs Fine-tuned Transformer Architecture
          </p>
        </div>
        <div className="bg-indigo-50 text-indigo-700 border border-indigo-100 px-3.5 py-1 rounded-full text-xs font-semibold self-start md:self-auto">
          Transformer Model Accuracy: +9.3% Accuracy Improvement
        </div>
      </div>

      {/* Comparison Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-900 text-white rounded-xl">
              <th className="p-3.5 rounded-l-xl font-bold">Model Architecture</th>
              <th className="p-3.5 text-center font-bold">Accuracy</th>
              <th className="p-3.5 text-center font-bold">Precision</th>
              <th className="p-3.5 text-center font-bold">Recall</th>
              <th className="p-3.5 text-center rounded-r-xl font-bold">F1 Score</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 font-medium text-slate-700">
            {evaluations.map((ev, idx) => {
              const isTransformer = ev.model_version.includes('Transformer') || ev.model_version.includes('DistilBERT');
              return (
                <tr 
                  key={ev.id || idx}
                  className={isTransformer ? 'bg-indigo-50/50 font-semibold text-slate-900' : 'hover:bg-slate-50'}
                >
                  <td className="p-3.5 flex items-center space-x-2">
                    {isTransformer ? (
                      <Award className="w-4 h-4 text-indigo-600" />
                    ) : (
                      <Zap className="w-4 h-4 text-slate-400" />
                    )}
                    <span>{ev.model_version}</span>
                  </td>
                  <td className="p-3.5 text-center text-indigo-600 font-bold">{ev.accuracy.toFixed(1)}%</td>
                  <td className="p-3.5 text-center">{ev.precision.toFixed(1)}%</td>
                  <td className="p-3.5 text-center">{ev.recall.toFixed(1)}%</td>
                  <td className="p-3.5 text-center text-emerald-600 font-bold">{ev.f1.toFixed(1)}%</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
