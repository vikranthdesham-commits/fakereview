import asyncio
import httpx
import re
from bs4 import BeautifulSoup

async def test_google_search_reviews():
    query = 'BVS Mandi Restaurant reviews'
    url = f'https://www.google.com/search?q={query.replace(" ", "+")}&hl=en'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        r = await client.get(url, headers=headers)
        print('Google Search Status:', r.status_code)
        
        # Save HTML to inspect
        with open('google_search.html', 'w', encoding='utf-8') as f:
            f.write(r.text)

        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Look for review spans or classes like '.J2Peb', '.review-snippet', '.K82p2e', etc.
        spans = soup.find_all('span')
        print(f"Total spans found: {len(spans)}")

        # Print spans with > 40 chars
        reviews = []
        for s in spans:
            txt = s.get_text().strip()
            if len(txt) > 35 and any(k in txt.lower() for k in ['food', 'mandi', 'taste', 'service', 'curry', 'money', 'poison', 'good', 'bad', 'place', 'order', 'restaurant']):
                if not any(bad in txt.lower() for bad in ['google', 'search', 'javascript', 'privacy', 'terms', 'sign in', 'maps']):
                    if txt not in reviews:
                        reviews.append(txt)

        print(f"\nExtracted {len(reviews)} real review snippets from Google Search:")
        for i, rev in enumerate(reviews[:15], 1):
            print(f"\n[{i}] {rev}")

if __name__ == '__main__':
    asyncio.run(test_google_search_reviews())
