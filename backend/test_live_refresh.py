import asyncio
from app.database import SessionLocal
from app.services.places_service import search_restaurant_place_id, get_restaurant_details

async def test_live_refresh():
    db = SessionLocal()
    try:
        print("\n--- STEP 1: SEARCHING MANDI LINK ---")
        pid1 = await search_restaurant_place_id("https://maps.app.goo.gl/nCrAfYjEGqtY2bGC9", db)
        d1 = await get_restaurant_details(pid1, db)
        print("RESULT 1 - Name:", d1["name"])
        print("RESULT 1 - Address:", d1["address"][:80])
        print("RESULT 1 - Review 1:", d1["reviews"][0]["text"][:120])

        print("\n--- STEP 2: SEARCHING DOMINOS PIZZA ---")
        pid2 = await search_restaurant_place_id("Dominos Pizza Hayathnagar", db)
        d2 = await get_restaurant_details(pid2, db)
        print("RESULT 2 - Name:", d2["name"])
        print("RESULT 2 - Address:", d2["address"][:80])
        print("RESULT 2 - Review 1:", d2["reviews"][0]["text"][:120])

        print("\n--- STEP 3: SEARCHING PARADISE BIRYANI ---")
        pid3 = await search_restaurant_place_id("Paradise Biryani Secunderabad", db)
        d3 = await get_restaurant_details(pid3, db)
        print("RESULT 3 - Name:", d3["name"])
        print("RESULT 3 - Address:", d3["address"][:80])
        print("RESULT 3 - Review 1:", d3["reviews"][0]["text"][:120])

    finally:
        db.close()

if __name__ == '__main__':
    asyncio.run(test_live_refresh())
