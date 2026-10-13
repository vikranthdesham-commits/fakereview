import React, { useEffect, useState } from 'react';
import ModelAblationCard from '../components/ModelAblationCard';
import FlaggedChart from '../components/FlaggedChart';
import { getAnalytics, getModelEvaluations } from '../utils/api';
import { BarChart3, ShieldCheck, AlertTriangle, Sparkles, Activity } from 'lucide-react';

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState(null);
  const [evaluations, setEvaluations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [anData, evData] = await Promise.all([
          getAnalytics(),
          getModelEvaluations()
        ]);
        setAnalytics(anData);
        setEvaluations(evData);
      } catch (err) {
        console.error('Analytics load error:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  return (
    <div className="space-y-8 pb-16">
      {/* Header Banner */}
      <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center space-x-2 bg-indigo-50 border border-indigo-100 text-indigo-700 font-semibold text-xs px-3 py-1 rounded-full mb-3">
            <BarChart3 className="w-3.5 h-3.5" />
            <span>Platform Telemetry & Model Benchmarks</span>
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            Analytics & Model Evaluation
          </h1>
          <p className="text-slate-600 text-sm mt-1 max-w-2xl">
            Track review analysis volumes, overall corpus authenticity rates, and ML model baseline comparisons in real time.
          </p>
        </div>
      </div>

      {/* Analytics Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-card space-y-1">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Reviews Analyzed</span>
          <p className="font-extrabold text-3xl text-slate-900">
            {analytics?.total_reviews_analyzed || 0}
          </p>
          <p className="text-xs text-slate-400">Across products & restaurants</p>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-card space-y-1">
          <span className="text-xs font-semibold text-rose-600 uppercase tracking-wider">Flagged Suspicious</span>
          <p className="font-extrabold text-3xl text-rose-600">
            {analytics?.suspicious_reviews_count || 0}
          </p>
          <p className="text-xs text-slate-400">Suspicion Index ≥ 45%</p>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-card space-y-1">
          <span className="text-xs font-semibold text-emerald-600 uppercase tracking-wider">Verified Genuine</span>
          <p className="font-extrabold text-3xl text-emerald-600">
            {analytics?.genuine_reviews_count || 0}
          </p>
          <p className="text-xs text-slate-400">Passed text & rating validation</p>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-card space-y-1">
          <span className="text-xs font-semibold text-indigo-600 uppercase tracking-wider">Average Suspicion Rate</span>
          <p className="font-extrabold text-3xl text-indigo-600">
            {analytics?.average_suspicion_score || 0}%
          </p>
          <p className="text-xs text-slate-400">Corpus normalized mean</p>
        </div>
      </div>

      {/* Model Benchmark Card */}
      <ModelAblationCard evaluations={evaluations} />

      {/* Authenticity Chart */}
      <FlaggedChart
        genuineCount={analytics?.genuine_reviews_count || 0}
        suspiciousCount={analytics?.suspicious_reviews_count || 0}
      />
    </div>
  );
}
