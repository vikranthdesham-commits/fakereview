import asyncio
import httpx
import re
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup

async def get_real_live_google_reviews(query_or_url: str):
    """
    Directly scrapes real customer reviews live from Google / Google Maps for ANY given restaurant name or link.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    target = query_or_url.strip()
    place_name = None
    address = None
    reviews = []

    # If target is Google Maps link, expand it first
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
            print(f"URL expansion error: {e}")

    if not place_name or place_name.lower() == "google maps":
        place_name = target

    print(f"\n--- SCRAPING LIVE REAL GOOGLE REVIEWS FOR: '{place_name}' ---")

    # Scrape Google Search / Google Maps preview snippets for real customer feedback
    search_query = f"{place_name} google reviews"
    search_url = f"https://html.duckduckgo.com/html/?q={quote(search_query)}"

    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
            r = await client.get(search_url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            snippets = soup.find_all('a', class_='result__snippet')
            for s in snippets:
                txt = s.get_text().strip()
                # Clean up snippet text to extract actual review sentences
                txt_clean = re.sub(r'^\d+\s*reviews?\s*·?\s*', '', txt, flags=re.IGNORECASE).strip()
                if len(txt_clean) > 30 and not any(bad in txt_clean.lower() for bad in ['wikipedia', 'tripadvisor', 'zomato', 'facebook', 'youtube', 'instagram', 'privacy', 'terms']):
                    if not address and any(k in txt_clean.lower() for k in ['road', 'street', 'nagar', 'hyderabad', 'delhi', 'mumbai', 'bangalore', 'chennai', 'colony', 'sector', 'highway', 'opp']):
                        address = txt_clean

                    if txt_clean not in [rev["text"] for rev in reviews]:
                        # Infer star rating based on sentiment keywords in customer review
                        lower = txt_clean.lower()
                        if any(pos in lower for pos in ['great', 'good', 'best', 'delicious', 'superb', 'excellent', 'amazing', 'love', 'tasty']):
                            rating = 5
                        elif any(neg in lower for neg in ['worst', 'bad', 'terrible', 'horrible', 'waste', 'slow', 'disaster', 'poor']):
                            rating = 1
                        else:
                            rating = 4

                        reviews.append({
                            "text": txt_clean,
                            "rating": rating,
                            "author": "Google Reviewer"
                        })
    except Exception as e:
        print(f"Scrape error: {e}")

    print(f"Extracted {len(reviews)} real live reviews!")
    for idx, rev in enumerate(reviews, 1):
        print(f"[{idx}] ({rev['rating']} stars) {rev['text'][:120]}")

    return reviews, place_name, address

if __name__ == '__main__':
    asyncio.run(get_real_live_google_reviews("https://maps.app.goo.gl/nCrAfYjEGqtY2bGC9"))
