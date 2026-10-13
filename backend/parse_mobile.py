import re
import json

def parse_mobile():
    with open('mobile_page.html', 'r', encoding='utf-8') as f:
        html = f.read()

    print("Search for place name in mobile HTML...")
    # Look for name matches
    names = re.findall(r'\"(BVS[^\"]{1,50}?)\"', html)
    print("Name matches:", set(names[:10]))

    # Search for reviews / strings in js data
    # Google Maps embeds review data arrays: [author, avatar_url, rating, "Review text...", time_str]
    # Let's search for string arrays in html
    reviews_found = []
    
    # Pattern to match review text blocks in Google Maps JS arrays
    # e.g., ["http...", "Author", ..., "The Currys here are SO delicious...", ...]
    matches = re.findall(r'\[\s*\"(https?://[^\"]+)\"\s*,\s*\"([^\"]+)\"\s*,.*?\"([^\"]{25,800}?)\"', html, re.DOTALL)
    print(f"Matched JS review structures: {len(matches)}")
    for m in matches[:5]:
        print(f"Author: {m[1]} | Review: {m[2][:100]}")

    # Search for any quoted text that contains food/review keywords
    quoted_texts = re.findall(r'\"([A-Z0-9][^\"]{30,600}?)\"', html)
    print(f"Total quoted texts: {len(quoted_texts)}")
    
    keywords = ["mandi", "food", "taste", "service", "curry", "currys", "money", "poison", "delicious", "mutton", "chicken", "price", "expensive"]
    filtered_reviews = []
    for qt in quoted_texts:
        qt_lower = qt.lower()
        if any(k in qt_lower for k in keywords):
            if not any(bad in qt_lower for bad in ["google", "function", "javascript", "window.", "schema", "http", "css", ".png", ".jpg"]):
                if qt not in filtered_reviews:
                    filtered_reviews.append(qt)

    print(f"\nFiltered Real Review Quotes Found: {len(filtered_reviews)}")
    for i, r in enumerate(filtered_reviews, 1):
        print(f"\n[{i}] {r}")

if __name__ == '__main__':
    parse_mobile()
