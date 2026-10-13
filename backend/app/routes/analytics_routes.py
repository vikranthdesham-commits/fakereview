from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.schemas.schemas import AnalyticsOverview, ModelEvaluationItem, HistoryItem
from app.models.models import ProductReview, ModelEvaluation, FallbackEvent

router = APIRouter(tags=["Analytics & Model Evaluations"])

@router.get("/analytics", response_model=AnalyticsOverview)
def get_analytics_overview(db: Session = Depends(get_db)):
    total = db.query(ProductReview).count()
    suspicious = db.query(ProductReview).filter(ProductReview.verdict == "Suspicious").count()
    genuine = db.query(ProductReview).filter(ProductReview.verdict == "Genuine").count()
    
    avg_score_res = db.query(func.avg(ProductReview.suspicion_score)).scalar()
    avg_score = float(avg_score_res) if avg_score_res else 0.0

    fallback_count = db.query(FallbackEvent).count()

    return {
        "total_reviews_analyzed": total,
        "suspicious_reviews_count": suspicious,
        "genuine_reviews_count": genuine,
        "average_suspicion_score": round(avg_score, 1),
        "fallback_event_count": fallback_count
    }

@router.get("/model-evaluations", response_model=List[ModelEvaluationItem])
def get_model_evaluations(db: Session = Depends(get_db)):
    evals = db.query(ModelEvaluation).order_by(ModelEvaluation.id.asc()).all()
    result = []
    for e in evals:
        result.append({
            "id": e.id,
            "model_version": e.model_version,
            "accuracy": e.accuracy,
            "precision": e.precision,
            "recall": e.recall,
            "f1": e.f1,
            "run_at": e.run_at.isoformat() if e.run_at else ""
        })
    return result

@router.get("/history", response_model=List[HistoryItem])
def get_analysis_history(db: Session = Depends(get_db)):
    history = db.query(ProductReview).order_by(ProductReview.created_at.desc()).limit(20).all()
    result = []
    for h in history:
        result.append({
            "id": h.id,
            "review_text": h.review_text,
            "suspicion_score": h.suspicion_score,
            "verdict": h.verdict,
            "confidence_level": h.confidence_level,
            "reasoning": h.reasoning,
            "created_at": h.created_at.isoformat() if h.created_at else ""
        })
    return result
