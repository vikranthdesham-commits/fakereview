import asyncio
from app.database import SessionLocal
from app.services.places_service import search_restaurant_place_id, get_restaurant_details

async def test():
    db = SessionLocal()
    try:
        url = 'https://maps.app.goo.gl/nCrAfYjEGqtY2bGC9'
        pid = await search_restaurant_place_id(url, db)
        details = await get_restaurant_details(pid, db)
        print('=== RESTAURANT SEARCH TEST ===')
        print('Place ID:', pid)
        print('Restaurant Name:', details['name'])
        print('Address:', details['address'])
        print('Trust Rating:', details['trust_adjusted_rating'])
        print('Flagged Pct:', details['flagged_percentage'])
        print('\n--- ALL REAL REVIEWS ANALYZED ---')
        for i, r in enumerate(details['reviews'], 1):
            print(f"[{i}] Rating: {r['rating']} stars | Score: {r['suspicion_score']}%")
            print(f"    Text: {r['text'][:140]}...\n")
    finally:
        db.close()

if __name__ == '__main__':
    asyncio.run(test())
