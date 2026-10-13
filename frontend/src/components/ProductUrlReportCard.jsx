import React, { useState } from 'react';
import { 
  ShieldCheck, AlertTriangle, ExternalLink, Star, Filter, Search, 
  CheckCircle2, XCircle, Tag, ShoppingBag, ArrowRightLeft, Sparkles, AlertCircle, Award, HelpCircle, Info
} from 'lucide-react';

export default function ProductUrlReportCard({ data, onNewSearch }) {
  const [activeFilter, setActiveFilter] = useState('all'); // 'all', 'fake', 'genuine'
  const [searchTerm, setSearchTerm] = useState('');
  const [showGradeGuide, setShowGradeGuide] = useState(true);

  if (!data || !data.product) return null;

  const {
    product,
    genuineness_score,
    trust_grade,
    original_rating,
    adjusted_rating,
    fake_review_count,
    genuine_review_count,
    total_reviews_analyzed,
    red_flags = [],
    rating_distribution = { original: {}, adjusted: {} },
    reviews = []
  } = data;

  // Grade color badges
  const gradeColorMap = {
    A: { bg: 'bg-emerald-600', border: 'border-emerald-500', text: 'text-emerald-600', lightBg: 'bg-emerald-50' },
    B: { bg: 'bg-teal-600', border: 'border-teal-500', text: 'text-teal-600', lightBg: 'bg-teal-50' },
    C: { bg: 'bg-amber-500', border: 'border-amber-400', text: 'text-amber-600', lightBg: 'bg-amber-50' },
    D: { bg: 'bg-orange-600', border: 'border-orange-500', text: 'text-orange-600', lightBg: 'bg-orange-50' },
    F: { bg: 'bg-rose-600', border: 'border-rose-500', text: 'text-rose-600', lightBg: 'bg-rose-50' },
  };

  const currentGradeTheme = gradeColorMap[trust_grade] || gradeColorMap.C;

  // Store Brand Styles
  const storeIsAmazon = product.store && product.store.toLowerCase().includes('amazon');
  const storeIsFlipkart = product.store && product.store.toLowerCase().includes('flipkart');

  const storeBtnLabel = storeIsAmazon 
    ? 'View Product on Amazon' 
    : storeIsFlipkart 
    ? 'View Product on Flipkart' 
    : 'View Product Page';

  const storeBtnClass = storeIsAmazon
    ? 'bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold shadow-lg shadow-amber-500/20'
    : storeIsFlipkart
    ? 'bg-blue-600 hover:bg-blue-500 text-white font-bold shadow-lg shadow-blue-600/20'
    : 'bg-indigo-600 hover:bg-indigo-500 text-white font-bold shadow-lg shadow-indigo-600/20';

  // Filter reviews
  const filteredReviews = reviews.filter((r) => {
    if (activeFilter === 'fake' && r.verdict !== 'Suspicious') return false;
    if (activeFilter === 'genuine' && r.verdict !== 'Genuine') return false;
    if (searchTerm) {
      const q = searchTerm.toLowerCase();
      return (
        r.reviewer_name.toLowerCase().includes(q) ||
        r.text.toLowerCase().includes(q) ||
        (r.highlighted_phrases && r.highlighted_phrases.some(p => p.toLowerCase().includes(q)))
      );
    }
    return true;
  });

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Product Summary Header Card */}
      <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-6 relative overflow-hidden">
        <div className="flex items-start sm:items-center space-x-5 z-10">
          {product.image && (
            <div className="w-24 h-24 sm:w-28 sm:h-28 rounded-2xl bg-white p-2.5 flex-shrink-0 flex items-center justify-center border-2 border-slate-700 shadow-xl overflow-hidden">
              <img src={product.image} alt={product.title} className="w-full h-full object-contain" />
            </div>
          )}
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center space-x-1.5 bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-3 py-0.5 rounded-full text-xs font-semibold">
                <ShoppingBag className="w-3.5 h-3.5 text-indigo-400" />
                <span>{product.store}</span>
              </span>
              {product.price && product.price !== 'N/A' && (
                <span className="text-xs font-bold text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-0.5 rounded-full">
                  {product.price}
                </span>
              )}
            </div>
            <h2 className="text-xl sm:text-2xl font-extrabold text-white leading-snug tracking-tight">
              {product.title}
            </h2>
            <div className="text-xs text-slate-400">
              <span>{total_reviews_analyzed} Customer Reviews Scanned</span>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap md:flex-col items-stretch sm:items-end gap-3 z-10">
          <a
            href={product.url}
            target="_blank"
            rel="noreferrer"
            className={`inline-flex items-center justify-center space-x-2 px-5 py-3 rounded-xl text-xs transition-all ${storeBtnClass}`}
          >
            <span>{storeBtnLabel}</span>
            <ExternalLink className="w-4 h-4" />
          </a>

          {onNewSearch && (
            <button
              onClick={onNewSearch}
              className="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold px-4 py-2.5 rounded-xl border border-slate-700 transition-all flex items-center justify-center space-x-1.5"
            >
              <span>Analyze Another Product</span>
            </button>
          )}
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* 1. Genuineness Trust Grade */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-card flex flex-col items-center justify-center text-center relative overflow-hidden">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
            Trust Grade & Score
          </span>
          <div className="flex items-center space-x-4 mb-2">
            <div className={`w-16 h-16 rounded-2xl ${currentGradeTheme.bg} text-white font-extrabold text-3xl flex items-center justify-center shadow-lg border-2 border-white/20`}>
              {trust_grade}
            </div>
            <div className="text-left">
              <div className="text-3xl font-extrabold text-slate-900 tracking-tight">
                {genuineness_score}%
              </div>
              <p className="text-xs font-semibold text-slate-500">Genuine Review Ratio</p>
            </div>
          </div>
          <p className="text-xs text-slate-500 mt-2 max-w-xs">
            Evaluated by ML language model trained to detect inauthentic text patterns and bot phrasing.
          </p>
        </div>

        {/* 2. Original vs Adjusted Star Rating */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-card flex flex-col justify-between space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Star Rating Audit
            </span>
            <ArrowRightLeft className="w-4 h-4 text-slate-400" />
          </div>

          <div className="grid grid-cols-2 gap-4 text-center divide-x divide-slate-100">
            <div className="pr-2">
              <span className="text-xs text-slate-400 font-semibold block mb-1">Store Rating</span>
              <div className="flex items-center justify-center space-x-1 text-amber-500 font-extrabold text-2xl">
                <span>{original_rating}</span>
                <Star className="w-5 h-5 fill-amber-400" />
              </div>
              <span className="text-[10px] text-slate-400 block mt-1">Official listing</span>
            </div>

            <div className="pl-2">
              <span className="text-xs text-indigo-600 font-semibold block mb-1">Adjusted Rating</span>
              <div className="flex items-center justify-center space-x-1 text-indigo-600 font-extrabold text-2xl">
                <span>{adjusted_rating}</span>
                <Star className="w-5 h-5 fill-indigo-600 text-indigo-600" />
              </div>
              <span className="text-[10px] text-slate-500 font-medium block mt-1">Excludes fake reviews</span>
            </div>
          </div>

          <div className="bg-slate-50 rounded-xl p-2.5 text-center text-xs text-slate-600 border border-slate-100">
            {original_rating > adjusted_rating ? (
              <span className="text-amber-700 font-medium">
                Rating inflated by <strong className="font-bold">{(original_rating - adjusted_rating).toFixed(1)}★</strong> due to suspicious promotional reviews.
              </span>
            ) : (
              <span className="text-emerald-700 font-medium">
                Adjusted rating closely matches official customer rating.
              </span>
            )}
          </div>
        </div>

        {/* 3. Review Breakdown Split */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-card flex flex-col justify-between space-y-4">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Review Audit Breakdown
          </span>

          <div className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center space-x-2 font-semibold text-slate-700">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Verified Genuine</span>
              </div>
              <span className="font-bold text-slate-900">{genuine_review_count} ({Math.round((genuine_review_count/total_reviews_analyzed)*100)}%)</span>
            </div>

            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center space-x-2 font-semibold text-slate-700">
                <XCircle className="w-4 h-4 text-rose-600" />
                <span>Flagged Suspicious</span>
              </div>
              <span className="font-bold text-rose-600">{fake_review_count} ({Math.round((fake_review_count/total_reviews_analyzed)*100)}%)</span>
            </div>

            {/* Visual Split Bar */}
            <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden flex">
              <div
                style={{ width: `${(genuine_review_count / total_reviews_analyzed) * 100}%` }}
                className="bg-emerald-500 h-full transition-all"
              />
              <div
                style={{ width: `${(fake_review_count / total_reviews_analyzed) * 100}%` }}
                className="bg-rose-500 h-full transition-all"
              />
            </div>
          </div>

          <div className="text-xs text-slate-500">
            Total {total_reviews_analyzed} reviews analyzed with SHAP feature attribution.
          </div>
        </div>
      </div>

      {/* Grade & Score Explanation Guide Card */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl p-6 shadow-xl border border-indigo-900/50 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Info className="w-5 h-5 text-indigo-400" />
            <h3 className="font-extrabold text-base text-white">
              Understanding Your Trust Grade ({trust_grade}) & Score ({genuineness_score}%)
            </h3>
          </div>
          <button
            onClick={() => setShowGradeGuide(!showGradeGuide)}
            className="text-xs text-indigo-300 hover:text-white underline font-semibold"
          >
            {showGradeGuide ? 'Hide Explanation' : 'Show Explanation'}
          </button>
        </div>

        {showGradeGuide && (
          <div className="space-y-4 text-xs leading-relaxed text-slate-300 pt-2 border-t border-indigo-900/60">
            <p>
              <strong className="text-white">What is the Genuineness Score?</strong> The score of <strong className="text-emerald-400">{genuineness_score}%</strong> means that out of all {total_reviews_analyzed} customer reviews analyzed for this product, <strong className="text-emerald-400">{genuineness_score}% were verified as real human buyer experiences</strong>. The remaining {100 - genuineness_score}% were flagged as suspicious (bot phrasing, paid reviews, or unverified seller spam).
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-5 gap-2 pt-1">
              <div className="bg-emerald-950/80 border border-emerald-800/80 p-2.5 rounded-xl text-center">
                <span className="font-bold text-emerald-400 text-sm block">Grade A</span>
                <span className="text-[10px] text-emerald-200">85% – 100% Genuine</span>
                <p className="text-[10px] text-slate-400 mt-1">Excellent trust. Natural organic reviews.</p>
              </div>
              <div className="bg-teal-950/80 border border-teal-800/80 p-2.5 rounded-xl text-center">
                <span className="font-bold text-teal-400 text-sm block">Grade B</span>
                <span className="text-[10px] text-teal-200">70% – 84% Genuine</span>
                <p className="text-[10px] text-slate-400 mt-1">Good trust. Safe to buy with minimal marketing noise.</p>
              </div>
              <div className="bg-amber-950/80 border border-amber-800/80 p-2.5 rounded-xl text-center">
                <span className="font-bold text-amber-400 text-sm block">Grade C</span>
                <span className="text-[10px] text-amber-200">55% – 69% Genuine</span>
                <p className="text-[10px] text-slate-400 mt-1">Moderate risk. Noticeable promotional reviews.</p>
              </div>
              <div className="bg-orange-950/80 border border-orange-800/80 p-2.5 rounded-xl text-center">
                <span className="font-bold text-orange-400 text-sm block">Grade D</span>
                <span className="text-[10px] text-orange-200">40% – 54% Genuine</span>
                <p className="text-[10px] text-slate-400 mt-1">High risk. Over half reviews show bot behavior.</p>
              </div>
              <div className="bg-rose-950/80 border border-rose-800/80 p-2.5 rounded-xl text-center">
                <span className="font-bold text-rose-400 text-sm block">Grade F</span>
                <span className="text-[10px] text-rose-200">&lt; 40% Genuine</span>
                <p className="text-[10px] text-slate-400 mt-1">Severe warning. Heavy fake review manipulation.</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* AI Red Flags Section with Detailed Red Explanation */}
      {red_flags && red_flags.length > 0 && (
        <div className="bg-rose-50/80 border-2 border-rose-300 rounded-3xl p-6 sm:p-7 shadow-lg space-y-5">
          <div className="flex items-center space-x-3 text-rose-900 font-extrabold text-lg">
            <div className="w-10 h-10 rounded-xl bg-rose-600 text-white flex items-center justify-center shadow-md">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div>
              <h3>AI Red Flags & Warning Signals Detected</h3>
              <p className="text-xs font-semibold text-rose-700 font-normal">Automated audit alerts raised by TrustGuard neural network model.</p>
            </div>
          </div>

          <ul className="space-y-2.5 text-xs sm:text-sm text-rose-950 font-semibold bg-white/70 p-4 rounded-2xl border border-rose-200 shadow-sm">
            {red_flags.map((flag, idx) => (
              <li key={idx} className="flex items-start space-x-2">
                <span className="text-rose-600 font-extrabold text-base">•</span>
                <span>{flag}</span>
              </li>
            ))}
          </ul>

          {/* Explanation Box for what the Red Paragraph/Box means */}
          <div className="bg-rose-900 text-white rounded-2xl p-5 shadow-md space-y-3">
            <div className="flex items-center space-x-2 text-amber-300 font-bold text-sm">
              <HelpCircle className="w-4 h-4 text-amber-300" />
              <h4>What Does This Red Section Mean? (Explanation for Users)</h4>
            </div>
            <p className="text-xs text-rose-100 leading-relaxed font-normal">
              This <strong className="text-white font-bold">Red Alert Box</strong> highlights critical <strong>manipulation warning signals</strong> found on the product listing page. Here is what each alert represents:
            </p>
            <ul className="space-y-2 text-xs text-rose-100 list-disc list-inside">
              <li>
                <strong className="text-white">Unverified Purchaser Surges:</strong> Indicates reviews written by accounts that did NOT purchase the item through verified store checkout.
              </li>
              <li>
                <strong className="text-white">Rating Inflation Gap:</strong> Shows how much the seller's official star rating (e.g. 4.6★) is artificially boosted compared to real human buyers (e.g. 3.3★).
              </li>
              <li>
                <strong className="text-white">Temporal Anomalies (Review Spikes):</strong> Multiple 5-star reviews posted within hours of each other, typical of paid review farms.
              </li>
              <li>
                <strong className="text-white">Repetitive Superlative Spam:</strong> Bot accounts posting identical or capitalized praise like <em>"AMAZING BEST EVER 100 STARS"</em>.
              </li>
            </ul>
          </div>
        </div>
      )}

      {/* Rating Distribution Comparison Chart */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-card space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h3 className="font-extrabold text-lg text-slate-900">Star Rating Distribution Comparison</h3>
            <p className="text-xs text-slate-500">Comparing original star breakdown vs trust-adjusted genuine stars.</p>
          </div>
          <div className="flex items-center space-x-4 text-xs font-semibold">
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-3 rounded bg-amber-400 inline-block" />
              <span className="text-slate-600">Original Distribution</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-3 rounded bg-indigo-600 inline-block" />
              <span className="text-slate-600">Adjusted Distribution</span>
            </div>
          </div>
        </div>

        <div className="space-y-3 pt-2">
          {[5, 4, 3, 2, 1].map((star) => {
            const origCount = rating_distribution.original?.[String(star)] || 0;
            const adjCount = rating_distribution.adjusted?.[String(star)] || 0;
            const maxVal = Math.max(total_reviews_analyzed, 1);

            return (
              <div key={star} className="space-y-1">
                <div className="flex items-center justify-between text-xs text-slate-700 font-semibold">
                  <span className="w-8 flex items-center space-x-1">
                    <span>{star}</span>
                    <Star className="w-3 h-3 text-amber-500 fill-amber-400" />
                  </span>
                  <div className="flex space-x-4 text-slate-500">
                    <span>Original: {origCount}</span>
                    <span>Adjusted: {adjCount}</span>
                  </div>
                </div>

                <div className="space-y-1">
                  {/* Original Bar */}
                  <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                    <div
                      style={{ width: `${(origCount / maxVal) * 100}%` }}
                      className="bg-amber-400 h-full rounded-full transition-all"
                    />
                  </div>
                  {/* Adjusted Bar */}
                  <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                    <div
                      style={{ width: `${(adjCount / maxVal) * 100}%` }}
                      className="bg-indigo-600 h-full rounded-full transition-all"
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Customer Reviews Dossier List */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-card space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-100">
          <div>
            <h3 className="font-extrabold text-xl text-slate-900">Scanned Customer Reviews</h3>
            <p className="text-xs text-slate-500 mt-0.5">Individual review inspection with SHAP highlighted phrases.</p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Filter Tabs */}
            <div className="inline-flex bg-slate-100 p-1 rounded-xl text-xs font-semibold text-slate-600">
              <button
                onClick={() => setActiveFilter('all')}
                className={`px-3 py-1.5 rounded-lg transition-all ${activeFilter === 'all' ? 'bg-white text-slate-900 shadow-sm' : 'hover:text-slate-900'}`}
              >
                All ({reviews.length})
              </button>
              <button
                onClick={() => setActiveFilter('fake')}
                className={`px-3 py-1.5 rounded-lg transition-all ${activeFilter === 'fake' ? 'bg-rose-600 text-white shadow-sm' : 'hover:text-rose-600'}`}
              >
                Flagged ({fake_review_count})
              </button>
              <button
                onClick={() => setActiveFilter('genuine')}
                className={`px-3 py-1.5 rounded-lg transition-all ${activeFilter === 'genuine' ? 'bg-emerald-600 text-white shadow-sm' : 'hover:text-emerald-600'}`}
              >
                Genuine ({genuine_review_count})
              </button>
            </div>

            {/* Search Input */}
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search reviews..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8 pr-3 py-1.5 rounded-xl border border-slate-200 text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-100"
              />
            </div>
          </div>
        </div>

        {/* Review Cards List */}
        <div className="space-y-4">
          {filteredReviews.length === 0 ? (
            <div className="text-center py-8 text-slate-500 text-sm">
              No reviews found matching the current filter.
            </div>
          ) : (
            filteredReviews.map((rev, idx) => {
              const isSuspicious = rev.verdict === 'Suspicious';

              return (
                <div
                  key={idx}
                  className={`p-5 rounded-2xl border transition-all space-y-3 ${
                    isSuspicious ? 'bg-rose-50/40 border-rose-200' : 'bg-slate-50/60 border-slate-200'
                  }`}
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center space-x-3">
                      <span className="font-bold text-sm text-slate-900">{rev.reviewer_name}</span>
                      {rev.is_verified ? (
                        <span className="bg-emerald-100 text-emerald-800 text-[11px] font-semibold px-2 py-0.5 rounded-full flex items-center space-x-1">
                          <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                          <span>Verified Purchase</span>
                        </span>
                      ) : (
                        <span className="bg-slate-200 text-slate-700 text-[11px] font-semibold px-2 py-0.5 rounded-full">
                          Unverified
                        </span>
                      )}
                      <span className="text-xs text-slate-400">{rev.date}</span>
                    </div>

                    <div className="flex items-center space-x-3">
                      {/* Star Rating */}
                      <div className="flex items-center text-amber-500 font-bold text-xs">
                        {Array.from({ length: 5 }).map((_, i) => (
                          <Star
                            key={i}
                            className={`w-3.5 h-3.5 ${i < rev.rating ? 'fill-amber-400 text-amber-400' : 'text-slate-300'}`}
                          />
                        ))}
                      </div>

                      {/* Verdict Badge */}
                      <span
                        className={`text-xs font-bold px-3 py-1 rounded-full border ${
                          isSuspicious
                            ? 'bg-rose-600 text-white border-rose-500 shadow-sm'
                            : 'bg-emerald-600 text-white border-emerald-500 shadow-sm'
                        }`}
                      >
                        {isSuspicious ? `Suspicious (${rev.suspicion_score}%)` : `Genuine (${rev.suspicion_score}%)`}
                      </span>
                    </div>
                  </div>

                  {/* Review Text */}
                  <p className="text-slate-800 text-sm leading-relaxed font-normal">
                    "{rev.text}"
                  </p>

                  {/* Highlighted Phrases */}
                  {rev.highlighted_phrases && rev.highlighted_phrases.length > 0 && (
                    <div className="flex flex-wrap items-center gap-1.5 pt-1">
                      <span className="text-xs font-semibold text-slate-500 flex items-center space-x-1">
                        <Tag className="w-3 h-3" />
                        <span>Highlighted Words:</span>
                      </span>
                      {rev.highlighted_phrases.map((phrase, pIdx) => (
                        <span
                          key={pIdx}
                          className={`text-xs px-2 py-0.5 rounded-md font-semibold border ${
                            isSuspicious
                              ? 'bg-rose-100 text-rose-800 border-rose-300'
                              : 'bg-slate-200 text-slate-800 border-slate-300'
                          }`}
                        >
                          {phrase}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Reasoning */}
                  <p className="text-xs text-slate-500 italic pt-1 border-t border-slate-200/60">
                    <strong className="font-semibold text-slate-600">AI Explanation:</strong> {rev.reasoning}
                  </p>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
