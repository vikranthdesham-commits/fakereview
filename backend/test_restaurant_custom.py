import httpx

def test_custom_restaurant():
    url = "http://127.0.0.1:8000/search-restaurant"
    
    # We test with a totally new restaurant query - "Sagar Ratna Restaurant"
    payload = {"query": "Sagar Ratna Restaurant"}
    print(f"Searching custom restaurant: {payload['query']}")
    
    resp = httpx.post(url, json=payload, timeout=15.0)
    print("Search status:", resp.status_code)
    data = resp.json()
    place_id = data.get("place_id")
    print("Generated Place ID:", place_id)
    
    if place_id:
        details_resp = httpx.get(f"http://127.0.0.1:8000/restaurant/{place_id}")
        print("Details status:", details_resp.status_code)
        details = details_resp.json()
        
        # Safe print for unicode/emoji
        def safe_str(val):
            return str(val).encode('ascii', errors='replace').decode('ascii')
            
        print("Restaurant Name:", safe_str(details.get("name")))
        print("Address:", safe_str(details.get("address")))
        print("Trust Adjusted Rating:", details.get("trust_adjusted_rating"))
        print("Flagged Pct:", details.get("flagged_percentage"))
        print("Source:", safe_str(details.get("source")))
        print("Total reviews:", len(details.get("reviews", [])))
        print("\nGeneric reviews preview:")
        for idx, r in enumerate(details.get("reviews", []), 1):
            text_safe = safe_str(r['text'])
            print(f"  {idx}. [Score: {r['suspicion_score']}%] - {text_safe[:110]}...")

if __name__ == '__main__':
    test_custom_restaurant()
