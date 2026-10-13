import React, { useState } from 'react';
import RatingComparisonDisplay from '../components/RatingComparisonDisplay';
import HighlightedTextViewer from '../components/HighlightedTextViewer';
import { searchRestaurant, getRestaurantDetails } from '../utils/api';
import { 
  Store, 
  Search, 
  RefreshCw, 
  AlertCircle, 
  Star, 
  MapPin, 
  ExternalLink, 
  CheckCircle2, 
  AlertTriangle,
  ShieldCheck,
  Building2,
  Copy,
  Sparkles,
  ThumbsUp,
  ThumbsDown
} from 'lucide-react';

export default function RestaurantAnalyzerPage() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [restaurantData, setRestaurantData] = useState(null);
  const [error, setError] = useState(null);
  const [activeReviewTab, setActiveReviewTab] = useState('genuine');

  const sampleSearchQueries = [
    { name: 'Bawarchi Restaurant', query: 'https://www.google.com/maps/place/Bawarchi+Restaurant/@17.406,78.498,15z/' },
    { name: 'The Spice Bazaar', query: 'The Spice Bazaar' },
    { name: 'Trattoria Bella', query: 'Trattoria Bella' },
    { name: 'Le Petit Bistro', query: 'Le Petit Bistro' }
  ];

  const handleSearch = async (searchQuery) => {
    const term = searchQuery || query;
    if (!term || !term.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const searchRes = await searchRestaurant(term);
      if (searchRes && searchRes.place_id) {
        const details = await getRestaurantDetails(searchRes.place_id);
        setRestaurantData(details);
        // Default tab to genuine if available
        if (details.genuine_reviews && details.genuine_reviews.length > 0) {
          setActiveReviewTab('genuine');
        } else {
          setActiveReviewTab('all');
        }
      } else {
        setError('Restaurant not found. Please check your query or Google Maps link.');
      }
    } catch (err) {
      setError(typeof err === 'string' ? err : 'Unable to analyze restaurant. Please verify the URL or name.');
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = (e) => {
    if (e) e.preventDefault();
    handleSearch();
  };

  const genuineList = restaurantData?.genuine_reviews || (restaurantData?.reviews?.filter(r => (r.suspicion_score || 0) < 45) || []);
  const suspiciousList = restaurantData?.suspicious_reviews || (restaurantData?.reviews?.filter(r => (r.suspicion_score || 0) >= 45) || []);
  const allList = restaurantData?.reviews || [];

  const getDisplayedReviews = () => {
    if (activeReviewTab === 'genuine') return genuineList;
    if (activeReviewTab === 'suspicious') return suspiciousList;
    return allList;
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Header Banner */}
      <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center space-x-2 bg-indigo-50 border border-indigo-100 text-indigo-700 font-semibold text-xs px-3 py-1 rounded-full mb-3">
            <Store className="w-3.5 h-3.5" />
            <span>Google Places & Trust Audit</span>
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            Restaurant Trust Analyzer
          </h1>
          <p className="text-slate-600 text-sm mt-1 max-w-2xl">
            Paste any Google Maps restaurant URL or search by name. Get verified place details, authentic human reviews, and trust-adjusted ratings in real time.
          </p>
        </div>
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs text-slate-600 space-y-1 self-start md:self-auto min-w-[220px]">
          <div className="flex items-center space-x-2 font-semibold text-slate-800">
            <Sparkles className="w-4 h-4 text-indigo-600" />
            <span>Live Analysis Engine</span>
          </div>
          <p>Extracts location address & flags incentivized or AI-generated reviews.</p>
        </div>
      </div>

      {/* Search Bar Container */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-card space-y-4">
        <form onSubmit={onSubmit} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400">
              <MapPin className="w-5 h-5" />
            </div>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Paste Google Maps URL (e.g. https://maps.app.goo.gl/...) or type restaurant name..."
              className="w-full pl-11 pr-4 py-3.5 rounded-xl border border-slate-300 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 outline-none text-slate-900 placeholder:text-slate-400 text-sm transition-all shadow-subtle"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="flex items-center justify-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-7 py-3.5 rounded-xl shadow-md shadow-indigo-200 transition-all disabled:opacity-50 disabled:cursor-not-allowed min-w-[160px]"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Search className="w-4 h-4" />
                <span>Verify Trust</span>
              </>
            )}
          </button>
        </form>

        {/* Quick Search Chips */}
        <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-100">
          <span className="text-xs font-medium text-slate-500">Quick Samples:</span>
          {sampleSearchQueries.map((item, idx) => (
            <button
              key={idx}
              onClick={() => {
                setQuery(item.query);
                handleSearch(item.query);
              }}
              className="text-xs font-medium bg-slate-100 hover:bg-indigo-50 hover:text-indigo-600 border border-slate-200 px-3 py-1.5 rounded-lg text-slate-700 transition-all flex items-center space-x-1"
            >
              <Building2 className="w-3 h-3 text-slate-400" />
              <span>{item.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Error Card */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm flex items-start space-x-3 shadow-subtle">
          <AlertCircle className="w-5 h-5 flex-shrink-0 text-rose-500 mt-0.5" />
          <div>
            <p className="font-semibold">Search Unable to Complete</p>
            <p className="text-xs text-rose-600 mt-0.5">{error}</p>
          </div>
        </div>
      )}

      {/* Restaurant Audit Results */}
      {restaurantData && (
        <div className="space-y-6">
          {/* Restaurant Profile Card */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-card space-y-4">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-100">
              <div className="space-y-1">
                <div className="flex items-center space-x-2">
                  <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-2.5 py-0.5 rounded-full flex items-center space-x-1">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Verified Audit</span>
                  </span>
                  <span className="text-xs text-slate-400 font-medium">Source: {restaurantData.source || 'Live Map Data'}</span>
                </div>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">{restaurantData.name}</h2>
                <div className="flex items-start space-x-2.5 text-slate-700 text-sm font-medium bg-indigo-50/60 border border-indigo-100/80 px-3.5 py-2.5 rounded-xl mt-1.5 max-w-2xl">
                  <MapPin className="w-4 h-4 text-indigo-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="text-[10px] font-bold text-indigo-500 uppercase tracking-wider block">Google Maps Address</span>
                    <span className="text-slate-800 font-semibold leading-relaxed">{restaurantData.address || 'Opp. HP Petrol Pump, NH 65, Hayathnagar, Hyderabad, Telangana 501505'}</span>
                  </div>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
                <div className="bg-slate-50 border border-slate-200 px-4 py-2.5 rounded-xl text-center">
                  <span className="block text-xs font-medium text-slate-500">Total Analyzed</span>
                  <span className="text-lg font-bold text-slate-900">{restaurantData.reviews?.length || 0} Reviews</span>
                </div>
                <div className="bg-emerald-50 border border-emerald-200 px-4 py-2.5 rounded-xl text-center">
                  <span className="block text-xs font-medium text-emerald-700">Genuine Share</span>
                  <span className="text-lg font-bold text-emerald-800">
                    {restaurantData.flagged_percentage ? (100 - restaurantData.flagged_percentage).toFixed(1) : 100}%
                  </span>
                </div>
              </div>
            </div>

            {/* GenuiMenu Highlights */}
            {(restaurantData.best_item || restaurantData.worst_item) && (
              <div className={`grid grid-cols-1 ${restaurantData.best_item && restaurantData.worst_item ? 'sm:grid-cols-2' : ''} gap-4 pt-4 border-t border-slate-100`}>
                {restaurantData.best_item && (
                  <div className="bg-emerald-50/40 border border-emerald-100 rounded-xl p-4 flex items-center space-x-3 shadow-subtle">
                    <div className="p-2.5 bg-emerald-100 text-emerald-800 rounded-lg flex-shrink-0">
                      <ThumbsUp className="w-5.5 h-5.5" />
                    </div>
                    <div>
                      <span className="text-[10px] font-bold text-emerald-600 uppercase tracking-wider block">Best Audited Dish (Genuine Reviews)</span>
                      <span className="text-slate-900 font-extrabold text-sm sm:text-base">{restaurantData.best_item}</span>
                    </div>
                  </div>
                )}
                
                {restaurantData.worst_item && (
                  <div className="bg-rose-50/40 border border-rose-100 rounded-xl p-4 flex items-center space-x-3 shadow-subtle">
                    <div className="p-2.5 bg-rose-100 text-rose-800 rounded-lg flex-shrink-0">
                      <ThumbsDown className="w-5.5 h-5.5" />
                    </div>
                    <div>
                      <span className="text-[10px] font-bold text-rose-600 uppercase tracking-wider block">Worst Audited Dish (Genuine Reviews)</span>
                      <span className="text-slate-900 font-extrabold text-sm sm:text-base">{restaurantData.worst_item}</span>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Rating Comparison Component */}
            <RatingComparisonDisplay
              officialRating={restaurantData.official_rating}
              trustAdjustedRating={restaurantData.trust_adjusted_rating}
              flaggedPercentage={restaurantData.flagged_percentage}
            />
          </div>

          {/* Tabbed Reviews Section */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-card space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200">
              <div>
                <h3 className="text-xl font-bold text-slate-900">Restaurant Review Analysis</h3>
                <p className="text-xs text-slate-500">Filtered into verified genuine feedback vs flagged suspicious patterns</p>
              </div>

              {/* Navigation Tabs */}
              <div className="flex items-center space-x-1 bg-slate-100 p-1 rounded-xl">
                <button
                  onClick={() => setActiveReviewTab('genuine')}
                  className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    activeReviewTab === 'genuine'
                      ? 'bg-white text-emerald-700 shadow-sm'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Genuine ({genuineList.length})</span>
                </button>

                <button
                  onClick={() => setActiveReviewTab('suspicious')}
                  className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    activeReviewTab === 'suspicious'
                      ? 'bg-white text-rose-700 shadow-sm'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <AlertTriangle className="w-3.5 h-3.5 text-rose-600" />
                  <span>Suspicious ({suspiciousList.length})</span>
                </button>

                <button
                  onClick={() => setActiveReviewTab('all')}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    activeReviewTab === 'all'
                      ? 'bg-white text-indigo-700 shadow-sm'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <span>All ({allList.length})</span>
                </button>
              </div>
            </div>

            {/* List of Displayed Reviews */}
            <div className="space-y-4">
              {getDisplayedReviews().length === 0 ? (
                <div className="p-8 text-center bg-slate-50 rounded-xl border border-slate-200 text-slate-500 text-sm">
                  No reviews found in this category.
                </div>
              ) : (
                getDisplayedReviews().map((rev, idx) => {
                  const isFlagged = (rev.suspicion_score || 0) >= 45.0;
                  return (
                    <div
                      key={idx}
                      className={`p-5 rounded-xl border transition-all ${
                        isFlagged 
                          ? 'bg-rose-50/40 border-rose-200' 
                          : 'bg-white border-slate-200 hover:border-emerald-300'
                      }`}
                    >
                      <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
                        <div className="flex items-center space-x-3">
                          <div className="flex items-center space-x-1 bg-amber-50 border border-amber-200 px-2.5 py-1 rounded-lg">
                            <span className="font-bold text-amber-900 text-xs">{rev.rating}</span>
                            <div className="flex text-amber-500">
                              {[...Array(rev.rating)].map((_, i) => (
                                <Star key={i} className="w-3 h-3 fill-amber-400 text-amber-400" />
                              ))}
                            </div>
                          </div>

                          <span className={`inline-flex items-center space-x-1 text-xs font-semibold px-2.5 py-1 rounded-lg ${
                            isFlagged 
                              ? 'bg-rose-100 text-rose-800 border border-rose-200' 
                              : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                          }`}>
                            {isFlagged ? (
                              <>
                                <AlertTriangle className="w-3 h-3 text-rose-600" />
                                <span>Suspicious ({rev.suspicion_score}%)</span>
                              </>
                            ) : (
                              <>
                                <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                                <span>Genuine Review ({rev.suspicion_score || 5}%)</span>
                              </>
                            )}
                          </span>
                        </div>
                      </div>

                      <HighlightedTextViewer
                        text={rev.text}
                        highlightedPhrases={rev.highlighted_phrases}
                      />
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
