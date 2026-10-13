import React from 'react';
import { ShieldCheck, Store, BarChart3, Search, CheckCircle2, AlertTriangle, ArrowRight, Sparkles, MapPin, Check, ShoppingBag } from 'lucide-react';

export default function HomePage({ setActiveTab }) {
  return (
    <div className="space-y-12 pb-16">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-8 sm:p-12 shadow-xl border border-indigo-950/50 relative overflow-hidden">
        <div className="max-w-3xl space-y-6 relative z-10">
          <div className="inline-flex items-center space-x-2 bg-indigo-500/10 border border-indigo-400/20 px-3.5 py-1 rounded-full text-indigo-300 font-semibold text-xs">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            <span>AI Review Authenticity & Trust Verification</span>
          </div>

          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight leading-tight text-white">
            Verify Any Restaurant or Product Review in Seconds.
          </h1>

          <p className="text-slate-300 text-base sm:text-lg leading-relaxed max-w-2xl font-normal">
            Paste any Google Maps link or e-commerce review text. TrustGuard identifies fake reviews, highlights exact manipulative wording, and calculates true trust-adjusted ratings.
          </p>

          <div className="flex flex-wrap gap-4 pt-4">
            <button
              onClick={() => setActiveTab('restaurant')}
              className="flex items-center space-x-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-6 py-3.5 rounded-xl shadow-lg shadow-indigo-600/30 transition-all"
            >
              <Store className="w-5 h-5 text-indigo-200" />
              <span>Verify Restaurant Link</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => setActiveTab('product')}
              className="flex items-center space-x-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-6 py-3.5 rounded-xl shadow-lg shadow-indigo-600/30 transition-all"
            >
              <ShoppingBag className="w-5 h-5 text-indigo-200" />
              <span>Verify Product Link</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </section>

      {/* Feature Cards Grid */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Restaurant Analyzer */}
        <div 
          onClick={() => setActiveTab('restaurant')}
          className="bg-white border border-slate-200 hover:border-indigo-300 rounded-2xl p-8 shadow-card hover:shadow-card-hover transition-all cursor-pointer group space-y-4"
        >
          <div className="w-12 h-12 rounded-xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 group-hover:scale-110 transition-all">
            <Store className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-extrabold text-2xl text-slate-900 group-hover:text-indigo-600 transition-colors">
              Restaurant Trust Analyzer
            </h3>
            <p className="text-xs font-medium text-slate-500 mt-1">
              Google Maps Link Paste • Name Search • Genuine Reviews
            </p>
          </div>
          <p className="text-sm text-slate-600 leading-relaxed">
            Paste any Google Maps URL (or search by restaurant name). Get the verified restaurant name, exact address, authentic customer reviews, and trust-adjusted star ratings.
          </p>
          <div className="flex items-center text-sm font-semibold text-indigo-600 pt-2 group-hover:translate-x-1 transition-transform">
            <span>Analyze Google Maps Link</span>
            <ArrowRight className="w-4 h-4 ml-1.5" />
          </div>
        </div>

        {/* Product Review Checker */}
        <div 
          onClick={() => setActiveTab('product')}
          className="bg-white border border-slate-200 hover:border-indigo-300 rounded-2xl p-8 shadow-card hover:shadow-card-hover transition-all cursor-pointer group space-y-4"
        >
          <div className="w-12 h-12 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600 group-hover:scale-110 transition-all">
            <Search className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-extrabold text-2xl text-slate-900 group-hover:text-emerald-600 transition-colors">
              Product URL & Review Checker
            </h3>
            <p className="text-xs font-medium text-slate-500 mt-1">
              Amazon & Flipkart Product Links • Trust Grades • Adjusted Ratings
            </p>
          </div>
          <p className="text-sm text-slate-600 leading-relaxed">
            Paste any Amazon or Flipkart product URL. Calculates Trust Grades (A-F), recalculates genuine star ratings excluding fake bot reviews, and highlights red flags.
          </p>
          <div className="flex items-center text-sm font-semibold text-emerald-600 pt-2 group-hover:translate-x-1 transition-transform">
            <span>Check Amazon or Flipkart URL</span>
            <ArrowRight className="w-4 h-4 ml-1.5" />
          </div>
        </div>
      </section>

      {/* Trust Guarantee Section */}
      <section className="bg-white border border-slate-200 rounded-2xl p-8 shadow-card space-y-6">
        <h3 className="font-extrabold text-xl text-slate-900">
          How TrustGuard Ensures Review Integrity
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div className="bg-slate-50 p-5 rounded-xl border border-slate-200/80 space-y-2">
            <div className="flex items-center space-x-2 text-indigo-600 font-bold">
              <Check className="w-4 h-4" />
              <span>Genuine vs Suspicious Split</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Separates real human reviews from suspicious promotional text so you read authentic experiences.
            </p>
          </div>
          <div className="bg-slate-50 p-5 rounded-xl border border-slate-200/80 space-y-2">
            <div className="flex items-center space-x-2 text-emerald-600 font-bold">
              <Check className="w-4 h-4" />
              <span>Location & Link Resolution</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Automatically parses Google Maps links, expanding shortlinks and fetching true address details.
            </p>
          </div>
          <div className="bg-slate-50 p-5 rounded-xl border border-slate-200/80 space-y-2">
            <div className="flex items-center space-x-2 text-indigo-600 font-bold">
              <Check className="w-4 h-4" />
              <span>XAI Explainable Intelligence</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Provides plain-English explanations of why a review was flagged or verified.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
