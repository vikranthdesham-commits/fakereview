import re
import json

def analyze_html():
    with open('scratch_page.html', 'r', encoding='utf-8') as f:
        html = f.read()

    print("--- PLACE NAME SEARCH ---")
    og = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if og:
        print("og:title:", og.group(1))

    title = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    if title:
        print("<title>:", title.group(1))

    # Look for google maps AF_initDataCallback or window.APP_INITIALIZATION_STATE
    print("\n--- REVIEWS SEARCH ---")
    
    # 1. Search for JSON-LD scripts
    json_ld = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html, re.DOTALL)
    print(f"JSON-LD blocks found: {len(json_ld)}")
    for j in json_ld:
        print("JSON-LD sample:", j[:200])

    # 2. Search for user reviews in jsdata / window arrays
    # Google Maps embeds reviews inside JS arrays like ["Reviewer Name", null, "Review text...", rating, ...]
    # Let's search for strings containing keywords like "Mandi", "service", "food", "taste", "money", "poison"
    review_snippets = []
    
    # Pattern for review text: text between 30 and 800 chars that looks like English sentences
    raw_strings = re.findall(r'\"([A-Z][^\"]{25,600}?[\.!\?])\"', html)
    print(f"Candidate sentence strings found: {len(raw_strings)}")
    
    keywords = ["mandi", "food", "taste", "service", "chicken", "mutton", "curry", "currys", "price", "money", "poison", "good", "bad", "worst"]
    for s in raw_strings:
        s_lower = s.lower()
        if any(kw in s_lower for kw in keywords) and not any(skip in s_lower for skip in ["google", "javascript", "cookies", "policy", "terms", "http"]):
            if s not in review_snippets:
                review_snippets.append(s)

    print(f"\nExtracted {len(review_snippets)} potential review snippets:")
    for i, r in enumerate(review_snippets[:10], 1):
        print(f"\n[{i}] {r}")

if __name__ == '__main__':
    analyze_html()
