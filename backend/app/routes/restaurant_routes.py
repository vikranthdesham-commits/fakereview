from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import (
    SearchRestaurantRequest,
    SearchRestaurantResponse,
    RestaurantDetailResponse
)
from app.services.places_service import search_restaurant_place_id, get_restaurant_details

router = APIRouter(tags=["Restaurant Trust Analyzer"])

@router.post("/search-restaurant", response_model=SearchRestaurantResponse)
async def search_restaurant(payload: SearchRestaurantRequest, db: Session = Depends(get_db)):
    """
    Search for restaurant by name or Google Maps link. Returns place_id.
    """
    cleaned = payload.query.strip() if payload.query else ""
    if not cleaned:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please enter a valid restaurant name or Google Maps link."
        )
    try:
        place_id = await search_restaurant_place_id(cleaned, db)
        return {"place_id": place_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to process restaurant query: {str(e)}"
        )


@router.get("/restaurant/{place_id}", response_model=RestaurantDetailResponse)
async def get_restaurant_info(place_id: str, db: Session = Depends(get_db)):
    """
    Get official rating, trust-adjusted rating, flagged review %, and detailed breakdown.
    """
    try:
        details = await get_restaurant_details(place_id, db)
        return details
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to retrieve restaurant details: {str(e)}"
        )
