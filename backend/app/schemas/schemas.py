from typing import List, Optional
from pydantic import BaseModel, Field

class AnalyzeReviewRequest(BaseModel):
    review_text: str = Field(..., min_length=1, description="Paste text of the review")

class AnalyzeReviewResponse(BaseModel):
    suspicion_score: float = Field(..., ge=0.0, le=100.0)
    verdict: str
    confidence: str
    reasoning: str
    highlighted_phrases: List[str]

class SearchRestaurantRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Restaurant name or Google Maps link")

class SearchRestaurantResponse(BaseModel):
    place_id: str

class RestaurantReviewItem(BaseModel):
    text: str
    rating: int
    suspicion_score: float
    highlighted_phrases: List[str]

class RestaurantDetailResponse(BaseModel):
    name: str
    address: Optional[str] = None
    google_maps_url: Optional[str] = None
    official_rating: float
    trust_adjusted_rating: float
    flagged_percentage: float
    reviews: List[RestaurantReviewItem] = []
    genuine_reviews: List[RestaurantReviewItem] = []
    suspicious_reviews: List[RestaurantReviewItem] = []
    source: str
    best_item: Optional[str] = None
    worst_item: Optional[str] = None

class ModelEvaluationItem(BaseModel):
    id: int
    model_version: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    run_at: str

class AnalyticsOverview(BaseModel):
    total_reviews_analyzed: int
    suspicious_reviews_count: int
    genuine_reviews_count: int
    average_suspicion_score: float
    fallback_event_count: int

class HistoryItem(BaseModel):
    id: int
    review_text: str
    suspicion_score: float
    verdict: str
    confidence_level: str
    reasoning: str
    created_at: str

class AnalyzeProductUrlRequest(BaseModel):
    url: str = Field(..., min_length=1, description="Paste Amazon, Flipkart, or Product URL")

class ProductInfo(BaseModel):
    title: str
    image: Optional[str] = None
    store: str
    price: Optional[str] = None
    original_rating: float
    url: str

class ProductReviewDetail(BaseModel):
    reviewer_name: str
    rating: int
    text: str
    date: str
    is_verified: bool
    suspicion_score: float
    verdict: str
    highlighted_phrases: List[str]
    reasoning: str

class AnalyzeProductUrlResponse(BaseModel):
    product: ProductInfo
    genuineness_score: float
    trust_grade: str
    original_rating: float
    adjusted_rating: float
    fake_review_count: int
    genuine_review_count: int
    total_reviews_analyzed: int
    red_flags: List[str]
    rating_distribution: dict
    reviews: List[ProductReviewDetail]

