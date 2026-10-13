import httpx

def test_long_url():
    url = "http://127.0.0.1:8000/search-restaurant"
    long_query = (
        "https://www.google.com/maps/place/B.TECH+BITES/@17.370283,78.5383422,12z/"
        "data=!4m10!1m2!2m1!1sRestaurants!3m6!1s0x3bcb0b7ca9ad6ca1:0x952084f66763b7f2!8m2!3d17.370283!"
        "4d78.6863928!15sCgtSZXN0YXVyYW50cyV5YW50c2VnZXN0X2N1bGlpYnJn%2FdBnTgAQA!16s%2Fg%2F11yztj94yl?"
        "entry=ttu&g_ep=EgoyMDI1MDMyNC4wASAFQAw%3D%3D"
    )
    
    print(f"Pasting long query (Length: {len(long_query)}):")
    print(long_query)
    
    payload = {"query": long_query}
    try:
        resp = httpx.post(url, json=payload, timeout=15.0)
        print("Search API Status code:", resp.status_code)
        data = resp.json()
        print("Response JSON:", data)
        
        place_id = data.get("place_id")
        if place_id:
            details_resp = httpx.get(f"http://127.0.0.1:8000/restaurant/{place_id}")
            print("Details API Status code:", details_resp.status_code)
            details = details_resp.json()
            print("Restaurant Name resolved:", details.get("name"))
            print("Total reviews fetched:", len(details.get("reviews", [])))
    except Exception as e:
        print("Error during request:", e)

if __name__ == '__main__':
    test_long_url()
