from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import (
    AnalyzeReviewRequest, AnalyzeReviewResponse,
    AnalyzeProductUrlRequest, AnalyzeProductUrlResponse
)
from app.services.ml_service import analyze_review_text
from app.services.product_scraper_service import analyze_product_url
from app.models.models import ProductReview

router = APIRouter(tags=["Product Review Analyzer"])

@router.post("/analyze-review", response_model=AnalyzeReviewResponse)
def analyze_review(payload: AnalyzeReviewRequest, db: Session = Depends(get_db)):
    """
    Platform-agnostic product review analyzer.
    Analyzes paste text and returns suspicion score, verdict, confidence, reasoning, and SHAP phrase highlights.
    """
    if not payload.review_text or not payload.review_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review text cannot be empty."
        )

    result = analyze_review_text(payload.review_text)

    # Persist in database
    try:
        review_record = ProductReview(
            review_text=payload.review_text.strip(),
            suspicion_score=result["suspicion_score"],
            verdict=result["verdict"],
            confidence_level=result["confidence"],
            reasoning=result["reasoning"]
        )
        db.add(review_record)
        db.commit()
    except Exception as e:
        print(f"Error persisting product review: {e}")
        db.rollback()

    return result

@router.post("/analyze-product-url", response_model=AnalyzeProductUrlResponse)
def analyze_product_url_endpoint(payload: AnalyzeProductUrlRequest, db: Session = Depends(get_db)):
    """
    Amazon & Flipkart Product URL Review Checker (Matching FakeReviewCheck.com).
    Extracts product metadata and customer reviews, calculates Trust Grade, Adjusted Rating, and AI Red Flags.
    """
    if not payload.url or not payload.url.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product URL cannot be empty."
        )

    try:
        result = analyze_product_url(payload.url)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process product URL: {str(e)}"
        )

