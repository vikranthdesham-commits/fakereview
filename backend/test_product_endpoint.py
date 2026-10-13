import requests

url = "http://127.0.0.1:8000/analyze-product-url"
payload = {
    "url": "https://www.amazon.in/Sparx-Sandal-Men-Comfort-Cotton/dp/B01N80K4A3"
}

print(f"Post payload to: {url}")
try:
    r = requests.post(url, json=payload, timeout=15)
    print("Status code:", r.status_code)
    data = r.json()
    product = data.get("product", {})
    
    def safe_str(val):
        if val is None:
            return "None"
        return str(val).encode('ascii', errors='replace').decode('ascii')
        
    print(f"Title: {safe_str(product.get('title'))}")
    print(f"Store: {safe_str(product.get('store'))}")
    print(f"Price: {safe_str(product.get('price'))}")
    print(f"Original Rating: {safe_str(product.get('original_rating'))}")
    print(f"Genuineness Score: {safe_str(data.get('genuineness_score'))}%")
    print(f"Trust Grade: {safe_str(data.get('trust_grade'))}")
    
    reviews = data.get("reviews", []) or []
    print(f"Total reviews: {len(reviews)}")
    for idx, r in enumerate(reviews[:3], 1):
        text_safe = safe_str(r['text'])
        name_safe = safe_str(r['reviewer_name'])
        print(f"  {idx}. {name_safe} ({r['rating']} stars) - {text_safe[:100]}...")
except Exception as e:
    print(f"Error checking API: {e}")
