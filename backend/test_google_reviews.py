import asyncio
import httpx
import re
import json

async def test_mobile_scrape():
    url = 'https://maps.app.goo.gl/nCrAfYjEGqtY2bGC9'
    mobile_headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        r = await client.get(url, headers=mobile_headers)
        print('Mobile Final URL:', str(r.url))
        print('Mobile HTML len:', len(r.text))

        # Check for title
        title = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE)
        if title:
            print("Title:", title.group(1))

        # Check for place name in og:title or meta
        og = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']', r.text, re.IGNORECASE)
        if og:
            print("og:title:", og.group(1))

        # Save mobile HTML to inspect
        with open('mobile_page.html', 'w', encoding='utf-8') as f:
            f.write(r.text)

if __name__ == '__main__':
    asyncio.run(test_mobile_scrape())
