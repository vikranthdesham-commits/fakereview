import React from 'react';
import { BookOpen, Cpu, ShieldCheck, Database, Sliders, Layers } from 'lucide-react';

export default function MethodologyPage() {
  return (
    <div className="space-y-8 pb-16">
      {/* Header Banner */}
      <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center space-x-2 bg-indigo-50 border border-indigo-100 text-indigo-700 font-semibold text-xs px-3 py-1 rounded-full mb-3">
            <BookOpen className="w-3.5 h-3.5" />
            <span>Architecture & Detection Methodology</span>
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            Methodology & Technical Architecture
          </h1>
          <p className="text-slate-600 text-sm mt-1 max-w-2xl">
            Detailed specifications on XAI token attribution, trust rating formulas, and Google Places link resolution.
          </p>
        </div>
      </div>

      <div className="space-y-6">
        {/* Section 1: Explainable AI SHAP */}
        <div className="bg-white border border-slate-200 rounded-2xl p-7 shadow-card space-y-3">
          <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <Cpu className="w-5 h-5 text-indigo-600" /> 1. Explainable AI & Feature Token Attribution
          </h3>
          <p className="text-slate-600 text-sm leading-relaxed">
            TrustGuard decomposes review text into token importances using <strong>SHAP (SHapley Additive exPlanations)</strong> combined with heuristic text analysis.
          </p>
          <ul className="list-disc list-inside text-xs text-slate-600 space-y-1.5 pt-1">
            <li><strong>Capitalization & Punctuation Ratios:</strong> Identifies excessive UPPERCASE text (&gt;35%) and repeated punctuation ("!!!").</li>
            <li><strong>Hype & Superlative Clustering:</strong> Detects repetitive ungrounded phrases ("best ever", "must buy wow").</li>
            <li><strong>Sentiment-to-Detail Ratio:</strong> Flags extreme positive or negative sentiment that lacks specific feature detail.</li>
          </ul>
        </div>

        {/* Section 2: Rating Formula */}
        <div className="bg-white border border-slate-200 rounded-2xl p-7 shadow-card space-y-3">
          <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <Sliders className="w-5 h-5 text-emerald-600" /> 2. Smooth Trust-Adjusted Rating Formula
          </h3>
          <p className="text-slate-600 text-sm leading-relaxed">
            Rather than hard-deleting reviews, TrustGuard calculates a weighted trust rating using continuous suspicion scores:
          </p>
          <div className="bg-slate-900 text-emerald-400 p-4 rounded-xl font-mono text-center text-xs sm:text-sm font-semibold border border-slate-800">
            trust_adjusted_rating = Σ( rating × (1 − suspicion_score) ) / Σ( 1 − suspicion_score )
          </div>
          <p className="text-xs text-slate-500 leading-relaxed">
            Reviews with higher suspicion scores ($0.0 \to 1.0$) contribute proportionally lower weight, shielding overall ratings from manipulation while preserving full audit visibility.
          </p>
        </div>

        {/* Section 3: Model Ablation Benchmark */}
        <div className="bg-white border border-slate-200 rounded-2xl p-7 shadow-card space-y-3">
          <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <Layers className="w-5 h-5 text-indigo-600" /> 3. Model Fine-Tuning & Benchmarks
          </h3>
          <p className="text-slate-600 text-sm leading-relaxed">
            Trained on benchmark fake review datasets (including Kaggle Fake Reviews and Ott et al. deceptive opinion spam). We benchmark a <strong>TF-IDF + Logistic Regression baseline</strong> (84.5% F1) against a <strong>Fine-Tuned DistilBERT Transformer</strong> (93.3% F1).
          </p>
        </div>

        {/* Section 4: Google Maps Link Resolution */}
        <div className="bg-white border border-slate-200 rounded-2xl p-7 shadow-card space-y-3">
          <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <Database className="w-5 h-5 text-slate-700" /> 4. Google Maps Link Resolution & Fallback Engine
          </h3>
          <p className="text-slate-600 text-sm leading-relaxed">
            Short Google Maps links (<code className="bg-slate-100 px-1.5 py-0.5 rounded text-slate-800">maps.app.goo.gl</code>) are unshortened server-side. The engine parses the HTML title and place metadata to extract the exact restaurant name and address before executing Google Places API or dynamic database queries.
          </p>
        </div>
      </div>
    </div>
  );
}
