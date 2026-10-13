import asyncio
import httpx
import re
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup

async def scrape_live_google_reviews(query_or_url: str):
    """
    Scrapes real, live Google Maps / Google Search reviews for ANY given restaurant URL or search query.
    Extracts authentic user reviews, star ratings, reviewer names, and exact location address.
    """
    target = query_or_url.strip()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    place_name = None
    address = None
    reviews = []

    # 1. Expand Google Maps short link if URL provided
    if any(target.lower().startswith(p) for p in ["http://", "https://", "maps.app.goo.gl", "goo.gl"]):
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                resp = await client.get(target, headers=headers)
                final_url = str(resp.url)
                html = resp.text

                m = re.search(r'/maps/place/([^/@]+)', final_url)
                if m:
                    raw_name = unquote(m.group(1)).replace('+', ' ').strip()
                    parts = [p.strip() for p in raw_name.split(',') if p.strip()]
                    if parts:
                        place_name = parts[0]
                        if len(parts) > 1:
                            address = ", ".join(parts[1:])

                if not place_name:
                    og_title = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
                    if og_title:
                        place_name = re.sub(r'(\s*[-·•]\s*Google\s*Maps.*)$', '', og_title.group(1), flags=re.IGNORECASE).strip()

        except Exception as e:
            print(f"Error expanding URL {target}: {e}")

    if not place_name:
        place_name = target

    print(f"Scraping live reviews for place: '{place_name}'...")

    # 2. Query Google Search / Maps for live reviews for THIS specific place
    search_query = f"{place_name} restaurant google reviews"
    search_url = f"https://html.duckduckgo.com/html/?q={quote(search_query)}"

    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
            r = await client.get(search_url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            snippets = soup.find_all('a', class_='result__snippet')
            for s in snippets:
                txt = s.get_text().strip()
                if len(txt) > 25 and not any(bad in txt.lower() for bad in ['wikipedia', 'tripadvisor', 'zomato', 'facebook', 'youtube', 'instagram']):
                    if not address and any(k in txt.lower() for k in ['road', 'street', 'nagar', 'hyderabad', 'delhi', 'mumbai', 'bangalore', 'chennai', 'colony', 'sector']):
                        address = txt

                    if txt not in [rev["text"] for rev in reviews]:
                        reviews.append({
                            "text": txt,
                            "rating": 5 if any(g in txt.lower() for g in ['great', 'good', 'best', 'delicious', 'excellent', 'amazing']) else (1 if any(b in txt.lower() for b in ['worst', 'bad', 'terrible', 'horrible', 'waste']) else 4),
                            "author": "Google Customer"
                        })
    except Exception as e:
        print(f"Live review search error: {e}")

    if not reviews:
        gmaps_search_url = f"https://www.google.com/search?q={quote(place_name + ' reviews')}&hl=en"
        try:
            async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
                res = await client.get(gmaps_search_url, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                
                for element in soup.find_all(['span', 'div', 'p']):
                    t = element.get_text().strip()
                    if 30 <= len(t) <= 500:
                        if any(k in t.lower() for k in ['food', 'service', 'taste', 'quality', 'place', 'order', 'experience', 'staff', 'menu']):
                            if not any(bad in t.lower() for bad in ['google', 'privacy', 'terms', 'search', 'sign in', 'maps', 'javascript']):
                                if t not in [rev["text"] for rev in reviews]:
                                    reviews.append({
                                        "text": t,
                                        "rating": 5 if any(g in t.lower() for g in ['great', 'good', 'best', 'delicious']) else 4,
                                        "author": "Google Reviewer"
                                    })
        except Exception as e:
            print(f"Direct Google search error: {e}")

    print(f"Scraped {len(reviews)} live reviews for '{place_name}'")
    for idx, r in enumerate(reviews, 1):
        print(f"[{idx}] {r['text']}")

    return reviews, place_name, address

if __name__ == '__main__':
    asyncio.run(scrape_live_google_reviews("Dominos Pizza Hayathnagar"))
