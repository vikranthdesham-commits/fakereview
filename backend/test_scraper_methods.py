import urllib.request
import re
from bs4 import BeautifulSoup
import json

headers_mobile = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

headers_desktop = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

def test_amazon_review_page(asin):
    url = f"https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    print("\nTesting Amazon Review Page:", url)
    req = urllib.request.Request(url, headers=headers_desktop)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        print("HTML length:", len(html))
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check title
        title_el = soup.find("a", {"data-hook": "product-link"}) or soup.find("title")
        if title_el:
            print("Title found:", title_el.get_text().strip()[:80])
            
        reviews = soup.find_all("div", {"data-hook": "review"})
        print("Review elements count:", len(reviews))
        for r in reviews[:3]:
            body = r.find("span", {"data-hook": "review-body"})
            name = r.find("span", {"class": "a-profile-name"})
            if body:
                print(" ->", name.get_text().strip() if name else "Anon", ":", body.get_text().strip()[:70])
    except Exception as e:
        print("Error:", e)

test_amazon_review_page("B08N5WRWNW")
