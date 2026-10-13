import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class ProductReview(Base):
    __tablename__ = "product_reviews"

    id = Column(Integer, primary_key=True, index=True)
    review_text = Column(Text, nullable=False)
    suspicion_score = Column(Float, nullable=False)  # 0 to 100
    verdict = Column(String(50), nullable=False)     # Genuine | Suspicious
    confidence_level = Column(String(50), nullable=False) # High | Medium | Low
    reasoning = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class RestaurantCache(Base):
    __tablename__ = "restaurants_cache"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=True)
    official_rating = Column(Float, nullable=False)
    adjusted_rating = Column(Float, nullable=False)
    flagged_pct = Column(Float, nullable=False)
    is_fallback_seed = Column(Boolean, default=False)
    last_fetched_at = Column(DateTime, default=datetime.datetime.utcnow)

    reviews = relationship("RestaurantReview", back_populates="restaurant", cascade="all, delete-orphan")

class RestaurantReview(Base):
    __tablename__ = "restaurant_reviews"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants_cache.id"), nullable=False)
    review_text = Column(Text, nullable=False)
    star_rating = Column(Integer, nullable=False)
    suspicion_score = Column(Float, nullable=False)
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)

    restaurant = relationship("RestaurantCache", back_populates="reviews")

class ModelEvaluation(Base):
    __tablename__ = "model_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String(100), nullable=False) # e.g. Baseline (TF-IDF + LogReg) vs Transformer (DistilBERT)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1 = Column(Float, nullable=False)
    run_at = Column(DateTime, default=datetime.datetime.utcnow)

class FallbackEvent(Base):
    __tablename__ = "fallback_events"

    id = Column(Integer, primary_key=True, index=True)
    searched_query = Column(Text, nullable=False)
    matched_restaurant_id = Column(Integer, ForeignKey("restaurants_cache.id"), nullable=True)
    failure_reason = Column(Text, nullable=False)
    triggered_at = Column(DateTime, default=datetime.datetime.utcnow)

    matched_restaurant = relationship("RestaurantCache")
