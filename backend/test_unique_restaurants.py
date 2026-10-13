import asyncio
from app.database import SessionLocal
from app.services.places_service import search_restaurant_place_id, get_restaurant_details

async def test_different_restaurants():
    db = SessionLocal()
    try:
        # Test 1: Mandi restaurant link / query
        pid1 = await search_restaurant_place_id("https://maps.app.goo.gl/nCrAfYjEGqtY2bGC9", db)
        d1 = await get_restaurant_details(pid1, db)
        
        # Test 2: Domino's Pizza
        pid2 = await search_restaurant_place_id("Domino's Pizza Hayathnagar", db)
        d2 = await get_restaurant_details(pid2, db)

        # Test 3: Paradise Biryani
        pid3 = await search_restaurant_place_id("Paradise Biryani Hyderabad", db)
        d3 = await get_restaurant_details(pid3, db)

        print("=== TEST 1: BVS MANDI / KARSH RESTAURANT ===")
        print("Name:", d1["name"])
        print("Address:", d1["address"])
        print("Review 1:", d1["reviews"][0]["text"])

        print("\n=== TEST 2: DOMINO'S PIZZA ===")
        print("Name:", d2["name"])
        print("Address:", d2["address"])
        print("Review 1:", d2["reviews"][0]["text"])

        print("\n=== TEST 3: PARADISE BIRYANI ===")
        print("Name:", d3["name"])
        print("Address:", d3["address"])
        print("Review 1:", d3["reviews"][0]["text"])

    finally:
        db.close()

if __name__ == '__main__':
    asyncio.run(test_different_restaurants())
