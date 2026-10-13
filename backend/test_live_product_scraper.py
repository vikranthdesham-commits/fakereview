import urllib.request
import re
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
}

def test_amazon_scrape(url):
    print("\n--- Testing Amazon URL ---")
    print("URL:", url)
    
    # Extract ASIN if Amazon
    asin_match = re.search(r'/(?:dp|product-reviews|gp/product)/([A-Z0-9]{10})', url)
    asin = asin_match.group(1) if asin_match else None
    print("Extracted ASIN:", asin)

    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        print("Fetched HTML length:", len(html))
        soup = BeautifulSoup(html, 'html.parser')
        
        title_el = soup.find(id="productTitle") or soup.find("meta", property="og:title")
        title = title_el.get_text().strip() if title_el else "Unknown Title"
        print("Title:", title[:80])
        
        img_el = soup.find(id="landingImage") or soup.find("meta", property="og:image")
        img = img_el.get('src') or img_el.get('content') if img_el else None
        print("Image:", img)
        
        # Scrape reviews
        reviews = []
        review_divs = soup.find_all("div", {"data-hook": "review"})
        print(f"Found {len(review_divs)} review elements on product page")
        for div in review_divs:
            body_el = div.find("span", {"data-hook": "review-body"})
            name_el = div.find("span", {"class": "a-profile-name"})
            rating_el = div.find("i", {"data-hook": "review-star-rating"}) or div.find("i", {"data-hook": "cmps-review-star-rating"})
            
            if body_el:
                review_text = body_el.get_text().strip()
                reviewer = name_el.get_text().strip() if name_el else "Amazon Customer"
                rating_str = rating_el.get_text() if rating_el else "5"
                rating = 5
                m = re.search(r'(\d+(?:\.\d+)?)', rating_str)
                if m:
                    rating = int(float(m.group(1)))
                    
                reviews.append({
                    "name": reviewer,
                    "rating": rating,
                    "text": review_text
                })
        print("Extracted reviews count:", len(reviews))
        for r in reviews[:3]:
            print("  *", r['name'], f"({r['rating']}★):", r['text'][:60])
            
    except Exception as e:
        print("Error fetching Amazon URL:", e)

test_amazon_scrape("https://www.amazon.in/dp/B08N5WRWNW")
