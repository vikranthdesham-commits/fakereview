import datetime
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models.models import RestaurantCache, RestaurantReview, ModelEvaluation, ProductReview
from app.services.ml_service import analyze_review_text

SEED_RESTAURANTS = [
    {
        "place_id": "ChIJN1t_rDeuEmsRUsoyG83frY4",
        "name": "The Spice Bazaar",
        "address": "142 Grand Culinary Ave, Downtown City Center, NY 10001",
        "official_rating": 4.6,
        "is_fallback_seed": True,
        "reviews": [
            {
                "text": "Authentic North Indian flavors! The butter chicken and garlic naan were fresh and rich in flavor. Cozy ambiance and prompt service.",
                "rating": 5
            },
            {
                "text": "AMAZING EXPERIENCE BEST FOOD IN TOWN FIVE STARS 10/10 MUST VISIT AGAIN WOW WOW WOW!!!",
                "rating": 5
            },
            {
                "text": "Good place for family dinners. Portion sizes are generous. Parking can be a challenge during weekend peak hours.",
                "rating": 4
            },
            {
                "text": "DO NOT EAT HERE TOTAL TRASH HORRIBLE FOOD SERVED COLD DISASTER SCAMMER OWNER!",
                "rating": 1
            },
            {
                "text": "The dal makhani was simmered well and had a smoky aroma. Service was courteous throughout our dinner.",
                "rating": 5
            }
        ]
    },
    {
        "place_id": "ChIJ3S-g4Bhv5zsR3k1eA8Xg_M8",
        "name": "Trattoria Bella",
        "address": "88 Olive Garden Way, Little Italy, San Francisco, CA 94133",
        "official_rating": 4.3,
        "is_fallback_seed": True,
        "reviews": [
            {
                "text": "Delicious handcrafted pasta and crisp thin-crust pizza. The tiramisu was light and balanced in sweetness.",
                "rating": 5
            },
            {
                "text": "UNBELIEVABLE ITALIAN FOOD BEST IN THE UNIVERSE SUPERB PERFECT PERFECT PERFECT 1000 STARS!",
                "rating": 5
            },
            {
                "text": "Nice rustic decor and friendly waitstaff. The wine selection was good though slightly pricey.",
                "rating": 4
            },
            {
                "text": "Pasta was alright but took nearly 40 minutes to arrive. Bread basket was fresh.",
                "rating": 3
            }
        ]
    },
    {
        "place_id": "ChIJ900g5Bhv5zsR4k1eA8Xg_M9",
        "name": "Le Petit Bistro",
        "address": "15 Rue de Gourmet, Arts District, Austin, TX 78701",
        "official_rating": 4.8,
        "is_fallback_seed": True,
        "reviews": [
            {
                "text": "Charming French café with delightful croissants and rich espresso. Great spot for a quiet brunch.",
                "rating": 5
            },
            {
                "text": "The onion soup was rich with caramelized depth and gooey gruyère cheese. Service was warm.",
                "rating": 5
            },
            {
                "text": "BEST BAKERY ON EARTH INSANELY GREAT LIFE CHANGING CROISSANTS BUY EVERYTHING TODAY WOW!",
                "rating": 5
            },
            {
                "text": "Seating is intimate and compact, but the steak frites were cooked to medium rare perfection.",
                "rating": 4
            }
        ]
    }
]

MODEL_EVALS = [
    {
        "model_version": "Baseline (TF-IDF + Logistic Regression)",
        "accuracy": 84.5,
        "precision": 82.1,
        "recall": 86.0,
        "f1": 84.0
    },
    {
        "model_version": "Fine-tuned Transformer (DistilBERT / RoBERTa)",
        "accuracy": 93.8,
        "precision": 92.5,
        "recall": 94.2,
        "f1": 93.3
    }
]

SAMPLE_PRODUCT_REVIEWS = [
    {
        "review_text": "The noise cancellation on these headphones is top tier. Easily blocks out subway and office chatter. Battery lasts around 28 hours on a single charge.",
        "suspicion_score": 8.5,
        "verdict": "Genuine",
        "confidence_level": "High",
        "reasoning": "Analyzed as genuine. Text exhibits detailed contextual description, natural syntax variation, and moderate emotional tone."
    },
    {
        "review_text": "BEST PHONE CASE EVER BUY NOW WOW FIVE STARS HIGHLY RECOMMENDED PERFECT QUALITY MUST BUY SCAM PROOF!!!",
        "suspicion_score": 96.4,
        "verdict": "Suspicious",
        "confidence_level": "High",
        "reasoning": "Flagged as suspicious due to: Excessive UPPERCASE characters (62% of text); Excessive punctuation marks (3 '!'); Repetitive extreme superlatives (best, wow, five stars); Overly extreme sentiment."
    }
]

def calculate_trust_rating(reviews_data):
    # trust_adjusted_rating = Σ(rating × (1 − suspicion_score)) / Σ(1 − suspicion_score)
    num = 0.0
    den = 0.0
    flagged_count = 0

    for r in reviews_data:
        score_norm = r["suspicion_score"] / 100.0
        weight = max(0.001, 1.0 - score_norm)
        num += r["rating"] * weight
        den += weight
        if r["suspicion_score"] >= 45.0:
            flagged_count += 1

    adj_rating = round(num / den, 2) if den > 0 else 0.0
    flagged_pct = round((flagged_count / len(reviews_data)) * 100.0, 1) if reviews_data else 0.0
    return adj_rating, flagged_pct

def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # 1. Seed Restaurants
        for item in SEED_RESTAURANTS:
            existing = db.query(RestaurantCache).filter(RestaurantCache.place_id == item["place_id"]).first()
            if not existing:
                # Calculate reviews analysis
                processed_reviews = []
                for rev in item["reviews"]:
                    analysis = analyze_review_text(rev["text"])
                    processed_reviews.append({
                        "text": rev["text"],
                        "rating": rev["rating"],
                        "suspicion_score": analysis["suspicion_score"],
                        "highlighted_phrases": analysis["highlighted_phrases"]
                    })

                adj_rating, flagged_pct = calculate_trust_rating(processed_reviews)

                rest = RestaurantCache(
                    place_id=item["place_id"],
                    name=item["name"],
                    address=item.get("address"),
                    official_rating=item["official_rating"],
                    adjusted_rating=adj_rating,
                    flagged_pct=flagged_pct,
                    is_fallback_seed=True,
                    last_fetched_at=datetime.datetime.utcnow()
                )
                db.add(rest)
                db.flush()

                for rev in processed_reviews:
                    r_obj = RestaurantReview(
                        restaurant_id=rest.id,
                        review_text=rev["text"],
                        star_rating=rev["rating"],
                        suspicion_score=rev["suspicion_score"],
                        fetched_at=datetime.datetime.utcnow()
                    )
                    db.add(r_obj)

        # 2. Seed Model Evaluations
        if db.query(ModelEvaluation).count() == 0:
            for me in MODEL_EVALS:
                db.add(ModelEvaluation(
                    model_version=me["model_version"],
                    accuracy=me["accuracy"],
                    precision=me["precision"],
                    recall=me["recall"],
                    f1=me["f1"],
                    run_at=datetime.datetime.utcnow()
                ))

        # 3. Seed Sample Product Reviews
        if db.query(ProductReview).count() == 0:
            for pr in SAMPLE_PRODUCT_REVIEWS:
                db.add(ProductReview(
                    review_text=pr["review_text"],
                    suspicion_score=pr["suspicion_score"],
                    verdict=pr["verdict"],
                    confidence_level=pr["confidence_level"],
                    reasoning=pr["reasoning"],
                    created_at=datetime.datetime.utcnow()
                ))

        db.commit()
        print("Database initialized and successfully seeded!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
