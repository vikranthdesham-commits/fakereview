import React, { useState } from 'react';
import ProductUrlReportCard from '../components/ProductUrlReportCard';
import { analyzeProductUrl } from '../utils/api';
import { ShieldCheck, Search, Sparkles, RefreshCw, AlertCircle, Link as LinkIcon, ShoppingBag } from 'lucide-react';

export default function ProductCheckerPage() {
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading]       = useState(false);
  const [urlResult, setUrlResult]   = useState(null);
  const [error, setError]           = useState(null);

  const handleAnalyze = async (e) => {
    if (e) e.preventDefault();
    if (!inputValue || !inputValue.trim()) return;

    setLoading(true);
    setError(null);
    setUrlResult(null);

    try {
      const data = await analyzeProductUrl(inputValue.trim());
      setUrlResult(data);
    } catch (err) {
      setError(typeof err === 'string' ? err : 'Failed to analyze product URL. Please check the link format.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Header Banner */}
      <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center space-x-2 bg-indigo-50 border border-indigo-100 text-indigo-700 font-semibold text-xs px-3 py-1 rounded-full mb-3">
            <ShoppingBag className="w-3.5 h-3.5" />
            <span>Amazon &amp; Flipkart Product Review Checker</span>
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            Product URL Checker
          </h1>
          <p className="text-slate-600 text-sm mt-1 max-w-2xl">
            Paste any Amazon or Flipkart product URL to inspect live customer reviews, calculate Trust Grade, recalculate true adjusted ratings, and spot bot manipulation instantly.
          </p>
        </div>
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs text-slate-600 space-y-1 self-start md:self-auto min-w-[220px]">
          <div className="flex items-center space-x-2 font-semibold text-slate-800">
            <Sparkles className="w-4 h-4 text-indigo-600" />
            <span>TrustGuard AI Standard</span>
          </div>
          <p>Scans Amazon &amp; Flipkart listings for review manipulation.</p>
        </div>
      </div>

      {/* Input Form Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-card space-y-4">
        <form onSubmit={handleAnalyze} className="space-y-4">
          <div>
            <label className="block text-sm font-bold text-slate-900 mb-2">
              Paste Amazon or Flipkart Product Link
            </label>
            <div className="relative">
              <input
                type="url"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="https://www.amazon.in/dp/... or https://www.flipkart.com/..."
                className="w-full pl-11 pr-4 py-3.5 rounded-xl border border-slate-300 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 outline-none text-slate-900 placeholder:text-slate-400 text-sm transition-all shadow-subtle font-mono text-xs sm:text-sm"
              />
              <LinkIcon className="w-5 h-5 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <button
              type="submit"
              disabled={loading || !inputValue.trim()}
              className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-7 py-3 rounded-xl shadow-md shadow-indigo-200 transition-all disabled:opacity-50 disabled:cursor-not-allowed text-sm"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Analyzing Product...</span>
                </>
              ) : (
                <>
                  <Search className="w-4 h-4" />
                  <span>Inspect Product URL</span>
                </>
              )}
            </button>
            {inputValue && (
              <button
                type="button"
                onClick={() => { setInputValue(''); setUrlResult(null); setError(null); }}
                className="text-xs font-semibold text-slate-500 hover:text-slate-900 px-3 py-2"
              >
                Clear
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Product URL Audit Report Card */}
      {urlResult && (
        <ProductUrlReportCard
          data={urlResult}
          onNewSearch={() => { setInputValue(''); setUrlResult(null); }}
        />
      )}
    </div>
  );
}
