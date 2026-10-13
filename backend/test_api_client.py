import httpx

def test_api():
    url = "http://127.0.0.1:8000/search-restaurant"
    resp = httpx.post(url, json={"query": "https://maps.app.goo.gl/nCrAfYjEGqtY2bGC9"}, timeout=15.0)
    data = resp.json()
    place_id = data["place_id"]
    print("Place ID:", place_id)

    details_resp = httpx.get(f"http://127.0.0.1:8000/restaurant/{place_id}")
    print("Details status:", details_resp.status_code)
    details = details_resp.json()

    print("Restaurant Name:", details.get("name"))
    print("Trust Adjusted Rating:", details.get("trust_adjusted_rating"))
    print("Flagged Pct:", details.get("flagged_percentage"))
    print("Total Reviews Count:", len(details.get("reviews", [])))
    print("\n--- REVIEWS RETURNED BY FASTAPI ENDPOINT ---")
    for i, r in enumerate(details.get("reviews", []), 1):
        print(f"[{i}] Star Rating: {r.get('rating')} | Suspicion Score: {r.get('suspicion_score')}%")
        print("    Review Content:", r.get("text"))
        print()

if __name__ == '__main__':
    test_api()
