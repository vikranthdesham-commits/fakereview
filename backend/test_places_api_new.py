import asyncio
import httpx
from app.config import settings

async def test_places_api_new():
    key = settings.GOOGLE_PLACES_API_KEY
    place_id = "ChIJG_3xjA-ayzsRFh3aJZ-Rbjg"

    url = f"https://places.googleapis.com/v1/places/{place_id}"
    headers = {
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": "id,displayName,formattedAddress,rating,reviews"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.get(url, headers=headers)
        data = res.json()
        print("Details status code:", res.status_code)
        reviews = data.get("reviews", [])
        print(f"Total Live Reviews Returned by Google: {len(reviews)}")
        for idx, rev in enumerate(reviews, 1):
            author = rev.get("authorAttribution", {}).get("displayName", "Google Reviewer")
            text = rev.get("originalText", {}).get("text") or rev.get("text", {}).get("text", "")
            rating = rev.get("rating", 5)
            print(f"[{idx}] ({rating}★) {author}: {text[:140]}...")

if __name__ == '__main__':
    asyncio.run(test_places_api_new())
