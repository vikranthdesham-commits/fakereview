import React from 'react';
import HighlightedTextViewer from './HighlightedTextViewer';
import { ShieldCheck, AlertTriangle, FileText, Sparkles, CheckCircle2, Clock } from 'lucide-react';

export default function CaseReportCard({ result, reviewText }) {
  if (!result) return null;

  const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const isSuspicious = result.verdict === 'Suspicious';

  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-card overflow-hidden transition-all">
      {/* Header Bar */}
      <div className="bg-slate-900 text-white px-6 py-3.5 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-4 h-4 text-indigo-400" />
          <span className="font-semibold tracking-wide text-white">TrustGuard AI Audit Result</span>
        </div>
        <div className="flex items-center space-x-2 text-slate-400">
          <Clock className="w-3.5 h-3.5" />
          <span>Analyzed at {timestamp}</span>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Top Metric & Verdict */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
          <div className="flex items-center space-x-4">
            <div className={`w-20 h-20 rounded-2xl flex flex-col items-center justify-center text-center p-2 border ${
              isSuspicious
                ? 'bg-rose-50 border-rose-200 text-rose-700'
                : 'bg-emerald-50 border-emerald-200 text-emerald-700'
            }`}>
              <span className="text-2xl font-extrabold leading-none">{result.suspicion_score}%</span>
              <span className="text-[10px] font-semibold tracking-wider uppercase mt-1">Suspicion</span>
            </div>

            <div>
              <div className="flex items-center space-x-2">
                <span className={`inline-flex items-center space-x-1 text-sm font-bold px-3 py-1 rounded-full ${
                  isSuspicious
                    ? 'bg-rose-100 text-rose-800 border border-rose-200'
                    : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                }`}>
                  {isSuspicious ? (
                    <>
                      <AlertTriangle className="w-4 h-4 text-rose-600" />
                      <span>Suspicious Review</span>
                    </>
                  ) : (
                    <>
                      <ShieldCheck className="w-4 h-4 text-emerald-600" />
                      <span>Verified Genuine</span>
                    </>
                  )}
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-1.5">
                Model Confidence: <span className="font-semibold text-slate-700">{result.confidence}</span>
              </p>
            </div>
          </div>
        </div>

        {/* Text Viewer */}
        <div className="space-y-2">
          <h4 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
            <FileText className="w-4 h-4 text-indigo-600" /> Review Text & Flagged Tokens
          </h4>
          <HighlightedTextViewer text={reviewText} highlightedPhrases={result.highlighted_phrases} />
        </div>

        {/* Reasoning Narrative */}
        <div className={`p-4 rounded-xl border ${
          isSuspicious 
            ? 'bg-rose-50/50 border-rose-200 text-slate-800' 
            : 'bg-emerald-50/50 border-emerald-200 text-slate-800'
        }`}>
          <h5 className="text-xs font-bold uppercase tracking-wider mb-1 flex items-center gap-1.5 text-slate-900">
            {isSuspicious ? (
              <AlertTriangle className="w-4 h-4 text-rose-600" />
            ) : (
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            )}
            AI Analysis Narrative
          </h5>
          <p className="text-xs sm:text-sm leading-relaxed text-slate-700">
            {result.reasoning}
          </p>
        </div>
      </div>
    </div>
  );
}
