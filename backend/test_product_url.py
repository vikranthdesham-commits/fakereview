import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.services.product_scraper_service import analyze_product_url

test_urls = [
    "https://www.amazon.in/Allen-Solly-Regular-Casual-Shirt/dp/B08N5WSHIRT",
    "https://www.amazon.in/Bacca-Bucci-Men-Casual-Sneakers/dp/B0CX12345",
    "https://www.amazon.com/Apple-iPhone-15-Pro-128GB/dp/B09V3KXJPB",
    "https://www.flipkart.com/noise-colorfit-pulse-2-max-smartwatch/p/itm12345",
    "https://www.amazon.in/LG-55-Inch-4K-OLED-TV/dp/B09V3TV"
]

for url in test_urls:
    print("=" * 60)
    print("Testing URL:", url)
    res = analyze_product_url(url)
    p = res["product"]
    print("Title:", p["title"])
    print("Store:", p["store"])
    print("Price:", p["price"].encode("ascii", "ignore").decode())
    print("Image URL:", p["image"])
    print(f"Trust Grade: {res['trust_grade']} ({res['genuineness_score']}%)")
    print("First Review:", res["reviews"][0]["reviewer_name"], "-", res["reviews"][0]["text"][:60])
