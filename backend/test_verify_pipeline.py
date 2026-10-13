import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
sys.path.append(os.path.dirname(__file__))

from app.services.product_scraper_service import analyze_product_url

urls = [
    # Scenario 1: Sample Preset URL (should match template)
    "https://www.amazon.in/dp/B08N5WRWNW", 
    # Scenario 2: Custom Sandal URL with 'cotton' in query/path (originally matched shirt, now sandal or search)
    "https://www.amazon.in/Sparx-Sandal-Men-Comfort-Cotton/dp/B01N80K4A3",
    # Scenario 3: Custom FlipFlop/Slide sandals URL
    "https://www.flipkart.com/yokohama-men-black-slides-sandals/p/itm123fake"
]

print("Starting Verification Tests...")
for url in urls:
    print("\n" + "="*80)
    print(f"ANALYZE URL: {url}")
    try:
        res = analyze_product_url(url)
        product = res.get("product", {})
        
        # Safely convert to ascii for Windows stdout
        def safe_str(val):
            if val is None:
                return "None"
            return str(val).encode('ascii', errors='replace').decode('ascii')
            
        print(f"Title: {safe_str(product.get('title'))}")
        print(f"Store: {safe_str(product.get('store'))}")
        print(f"Price: {safe_str(product.get('price'))}")
        print(f"Original Rating: {safe_str(product.get('original_rating'))}")
        print(f"Genuineness Score: {safe_str(res.get('genuineness_score'))}%")
        print(f"Trust Grade: {safe_str(res.get('trust_grade'))}")
        
        reviews = res.get("reviews", []) or []
        print(f"Total reviews analyzed: {len(reviews)}")
        print("Reviews List:")
        for idx, r in enumerate(reviews[:3], 1):
            text_safe = safe_str(r['text'])
            name_safe = safe_str(r['reviewer_name'])
            print(f"  {idx}. {name_safe} ({r['rating']} stars) - {text_safe[:120]}...")
            
    except Exception as e:
        print(f"Error in test logic: {e}")
