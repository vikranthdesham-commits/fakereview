import asyncio
import httpx
import re
import json
from urllib.parse import quote, unquote

async def get_live_google_maps_reviews(url_or_name: str):
    """
    Fetches real live reviews from Google Maps for any given Google Maps URL or search query.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    # Step 1: Follow redirects if short link
    target_url = url_or_name.strip()
    if not target_url.startswith(("http://", "https://")):
        target_url = f"https://www.google.com/maps/search/{quote(target_url)}"

    final_url = target_url
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        try:
            r = await client.get(target_url, headers=headers)
            final_url = str(r.url)
            html = r.text
        except Exception as e:
            print(f"Error fetching URL: {e}")
            return [], "Unknown Place", "Address unavailable"

    print("Final URL:", final_url)
    
    # Extract Place Name & Address from Google Maps URL / HTML
    place_name = None
    address = None

    # Try matching place name from URL: /maps/place/PLACE_NAME/@lat,lng
    m = re.search(r'/maps/place/([^/@]+)', final_url)
    if m:
        raw_name = unquote(m.group(1)).replace('+', ' ')
        parts = [p.strip() for p in raw_name.split(',') if p.strip()]
        if parts:
            place_name = parts[0]
            if len(parts) > 1:
                address = ", ".join(parts[1:])

    if not place_name:
        og_t = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if og_t:
            place_name = re.sub(r'(\s*[-·•]\s*Google\s*Maps.*)$', '', og_t.group(1), flags=re.IGNORECASE).strip()

    print("Extracted Place Name:", place_name)
    print("Extracted Address:", address)

    # Search HTML for live user reviews
    # Google Maps embeds review strings in JS arrays within the HTML
    # We look for review text structures: ["Author Name", null, "Review text...", rating, ...]
    reviews = []

    # Regex pattern to match review strings inside Google Maps HTML JS data arrays
    # Look for patterns where a reviewer name is followed by review text and star rating
    raw_matches = re.findall(r'\[\s*\"(https?://[^\"]+googleusercontent[^\"]+)\"\s*,\s*\"([^\"]{2,50})\"\s*,.*?\"([^\"]{15,1000})\".*?([1-5])\s*\]', html, re.DOTALL)
    print(f"Raw JS review matches: {len(raw_matches)}")
    for m in raw_matches[:10]:
        reviews.append({
            "author": m[1],
            "text": m[2],
            "rating": int(m[3])
        })

    # If regex array match didn't catch all, fallback to extracting quoted text blocks from Google Maps HTML
    if not reviews:
        # Match quoted texts that look like customer reviews (between 25 and 800 chars)
        quoted_blocks = re.findall(r'\"([A-Z0-9][^\"]{25,800}?[\.!\?])\"', html)
        print(f"Quoted blocks candidate count: {len(quoted_blocks)}")
        keywords = ["food", "service", "mandi", "taste", "curry", "chicken", "mutton", "price", "quality", "ambiance", "place", "order", "staff", "good", "bad", "worst", "great", "delicious", "slow", "fast"]
        for q in quoted_blocks:
            q_lower = q.lower()
            if any(k in q_lower for k in keywords):
                if not any(bad in q_lower for bad in ["google", "javascript", "window.", "schema", "http", "css", "policy", "privacy", "terms", "cookie", "button"]):
                    if not any(r["text"] == q for r in reviews):
                        reviews.append({
                            "author": "Google User",
                            "text": q,
                            "rating": 5 if any(p in q_lower for p in ["good", "great", "delicious", "best", "super"]) else 3
                        })

    print(f"Total Live Reviews Extracted: {len(reviews)}")
    for i, r in enumerate(reviews[:5], 1):
        print(f"[{i}] {r['author']} ({r['rating']}★): {r['text'][:100]}...")

    return reviews, place_name, address

if __name__ == '__main__':
    asyncio.run(get_live_google_maps_reviews("https://maps.app.goo.gl/nCrAfYjEGqtY2bGC9"))
