import requests
import re
from bs4 import BeautifulSoup

headers_desktop = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/',
}

def test_scrape(url):
    print("\n" + "="*50)
    print("Fetching:", url)
    try:
        r = requests.get(url, headers=headers_desktop, timeout=10)
        print("Status Code:", r.status_code)
        print("Response Length:", len(r.text))
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Title check
        title_el = soup.find(id="productTitle") or soup.find("h1") or soup.find("meta", property="og:title") or soup.find("title")
        title_text = title_el.get_text().strip() if hasattr(title_el, 'get_text') else (title_el.get('content', '') if title_el else '')
        print("Extracted Title:", title_text[:100])
        
        # Check if we can find any reviews
        amazon_reviews = soup.find_all("div", {"data-hook": "review"})
        print(f"Amazon review elements found: {len(amazon_reviews)}")
        
        # Flipkart review check
        # Flipkart reviews are often in divs with class col, or _2wU5z or similar, but let's see classes that look like reviews
        flipkart_reviews = []
        for d in soup.find_all("div"):
            # Flipkart review body is inside class 'ZmyHe0' or 't-yD1y' or similar
            cls = d.get('class', [])
            if any('ZmyHe0' in c or 't-yD1y' in c for c in cls):
                flipkart_reviews.append(d.get_text().strip())
        print(f"Flipkart review elements found by class guess: {len(flipkart_reviews)}")
        
        # If no reviews, try finding standard review elements or text areas that look like reviews
        gen_comments = []
        for element in soup.find_all(['span', 'p', 'div']):
            t = element.get_text().strip()
            # If line is longer and mentions words like buy, product, quality, good, bad, etc.
            if 30 <= len(t) <= 300:
                if any(w in t.lower() for w in ['quality', 'recommend', 'product', 'material', 'comfortable', 'fit', 'size', 'colour', 'price']):
                    if not any(bad in t.lower() for bad in ['javascript', 'cookie', 'robot check', 'security', 'amazon', 'flipkart', 'browser', 'terms', 'privacy']):
                        if t not in gen_comments:
                            gen_comments.append(t)
        print(f"General candidate reviews from text: {len(gen_comments)}")
        for c in gen_comments[:3]:
            print("  *", c)
            
    except Exception as e:
        print("Error:", e)

# Test with a live Amazon sandles link and a Flipkart sandles link
test_scrape("https://www.amazon.in/Sparx-Sandal-Men-Comfort-Cotton/dp/B01N80K4A3")
test_scrape("https://www.flipkart.com/crocs-classic-clogs-etc/p/itm123")
