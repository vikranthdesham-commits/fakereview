import React from 'react';
import { Star, ShieldCheck, AlertTriangle, TrendingDown, Info } from 'lucide-react';

export default function RatingComparisonDisplay({ officialRating, trustAdjustedRating, flaggedPercentage }) {
  const delta = (officialRating - trustAdjustedRating).toFixed(2);
  const isInflated = delta > 0.1;

  return (
    <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <h3 className="font-extrabold text-lg text-slate-900">Trust Rating Comparison</h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Calculated by filtering fake review bias: Σ(rating × (1 − suspicion)) / Σ(1 − suspicion)
          </p>
        </div>
        {isInflated && (
          <div className="flex items-center space-x-2 bg-amber-50 text-amber-800 border border-amber-200 px-3.5 py-1.5 rounded-lg text-xs font-semibold self-start md:self-auto">
            <TrendingDown className="w-4 h-4 text-amber-600" />
            <span>Unfiltered Rating Inflated by +{delta} Stars</span>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        {/* Official Google Rating */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-subtle text-center space-y-1">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Official Google Rating
          </span>
          <div className="flex items-center justify-center space-x-1.5 pt-1">
            <span className="font-extrabold text-3xl text-slate-900">{officialRating.toFixed(1)}</span>
            <Star className="w-6 h-6 text-amber-400 fill-amber-400" />
          </div>
          <p className="text-xs text-slate-400 pt-1">Unfiltered Average</p>
        </div>

        {/* Authentic Trust Rating */}
        <div className="bg-gradient-to-br from-indigo-900 to-slate-900 text-white p-5 rounded-xl border border-indigo-950 shadow-md text-center space-y-1 relative overflow-hidden">
          <div className="absolute top-2 right-2 text-indigo-400/20">
            <ShieldCheck className="w-12 h-12" />
          </div>
          <span className="text-xs font-semibold text-indigo-200 uppercase tracking-wider relative z-10">
            Authentic Trust Score
          </span>
          <div className="flex items-center justify-center space-x-1.5 pt-1 relative z-10">
            <span className="font-extrabold text-3xl text-emerald-400">
              {trustAdjustedRating.toFixed(2)}
            </span>
            <Star className="w-6 h-6 text-emerald-400 fill-emerald-400" />
          </div>
          <p className="text-xs text-indigo-200/80 pt-1 relative z-10">Suspicion-Weighted Rating</p>
        </div>

        {/* Flagged Suspicious Reviews */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-subtle text-center space-y-2">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Flagged Fake / AI Reviews
          </span>
          <div className="flex items-center justify-center space-x-1.5 pt-0.5">
            <span className={`font-extrabold text-3xl ${flaggedPercentage > 25 ? 'text-rose-600' : 'text-emerald-600'}`}>
              {flaggedPercentage}%
            </span>
            {flaggedPercentage > 25 ? (
              <AlertTriangle className="w-6 h-6 text-rose-500" />
            ) : (
              <ShieldCheck className="w-6 h-6 text-emerald-500" />
            )}
          </div>
          <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
            <div 
              className={`h-full transition-all ${flaggedPercentage > 25 ? 'bg-rose-500' : 'bg-emerald-500'}`}
              style={{ width: `${Math.min(100, flaggedPercentage)}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
