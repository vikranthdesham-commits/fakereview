import React, { useEffect, useState } from 'react';
import { getHistory } from '../utils/api';
import { History, FileText, AlertTriangle, CheckCircle2, RefreshCw, Clock } from 'lucide-react';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchHistory() {
      try {
        const data = await getHistory();
        setHistory(data);
      } catch (err) {
        console.error('Failed to load audit history:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchHistory();
  }, []);

  return (
    <div className="space-y-8 pb-16">
      {/* Header Banner */}
      <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center space-x-2 bg-indigo-50 border border-indigo-100 text-indigo-700 font-semibold text-xs px-3 py-1 rounded-full mb-3">
            <History className="w-3.5 h-3.5" />
            <span>Audit History & Case Trail</span>
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            Analysis History
          </h1>
          <p className="text-slate-600 text-sm mt-1 max-w-2xl">
            Log of previously submitted product and restaurant review verification runs.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center py-16 text-slate-500 text-sm">
          <RefreshCw className="w-5 h-5 animate-spin mr-2 text-indigo-600" />
          <span>Retrieving analysis logs...</span>
        </div>
      ) : history.length === 0 ? (
        <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center text-slate-500 text-sm shadow-card space-y-2">
          <p className="font-semibold text-slate-800">No previous audits found</p>
          <p className="text-xs">Inspect a restaurant link or product review text to generate an audit log.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {history.map((item) => {
            const isSuspicious = item.verdict === 'Suspicious';
            return (
              <div
                key={item.id}
                className={`bg-white border rounded-2xl p-6 shadow-card space-y-3 transition-all ${
                  isSuspicious ? 'border-rose-200 hover:border-rose-300' : 'border-slate-200 hover:border-emerald-300'
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 text-xs">
                  <div className="flex items-center space-x-2">
                    <FileText className="w-4 h-4 text-indigo-600" />
                    <span className="font-bold text-slate-900">AUDIT LOG #{item.id}</span>
                    <span className="text-slate-300">•</span>
                    <div className="flex items-center space-x-1 text-slate-400">
                      <Clock className="w-3.5 h-3.5" />
                      <span>{new Date(item.created_at).toLocaleString()}</span>
                    </div>
                  </div>

                  <span className={`font-semibold px-3 py-1 rounded-full text-xs flex items-center space-x-1 ${
                    isSuspicious 
                      ? 'bg-rose-100 text-rose-800 border border-rose-200' 
                      : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                  }`}>
                    {isSuspicious ? (
                      <AlertTriangle className="w-3.5 h-3.5 text-rose-600" />
                    ) : (
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                    )}
                    <span>{item.verdict} ({item.suspicion_score}%)</span>
                  </span>
                </div>

                <p className="text-sm text-slate-800 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-200">
                  "{item.review_text}"
                </p>

                <p className="text-xs text-slate-600">
                  <strong className="font-semibold text-slate-900">AI Explanation: </strong>
                  {item.reasoning}
                </p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
