import asyncio
import httpx
from app.config import settings

async def test_google_places_api():
    key = settings.GOOGLE_PLACES_API_KEY
    print("Testing Google Places API with key:", key[:10] + "...")

    # Find Place
    search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": "Dominos Pizza Hayathnagar",
        "inputtype": "textquery",
        "fields": "place_id,name,rating,formatted_address",
        "key": key
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(search_url, params=params)
        data = r.json()
        print("\n=== GOOGLE PLACES SEARCH RESPONSE ===")
        print("Status:", data.get("status"))
        if data.get("status") == "OK" and data.get("candidates"):
            cand = data["candidates"][0]
            place_id = cand["place_id"]
            print("Place ID:", place_id)
            print("Name:", cand.get("name"))
            print("Address:", cand.get("formatted_address"))
            print("Rating:", cand.get("rating"))

            # Place Details & Reviews
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            d_params = {
                "place_id": place_id,
                "fields": "name,rating,formatted_address,reviews",
                "key": key
            }
            dr = await client.get(details_url, params=d_params)
            d_data = dr.json()
            print("\n=== GOOGLE PLACES DETAILS RESPONSE ===")
            print("Status:", d_data.get("status"))
            if d_data.get("status") == "OK" and "result" in d_data:
                res = d_data["result"]
                reviews = res.get("reviews", [])
                print(f"Total Live Google Reviews: {len(reviews)}")
                for idx, rev in enumerate(reviews, 1):
                    print(f"[{idx}] ({rev.get('rating')}★) {rev.get('author_name')}: {rev.get('text')[:120]}...")
        else:
            print("Error message:", data.get("error_message", "No candidates found"))

if __name__ == '__main__':
    asyncio.run(test_google_places_api())
