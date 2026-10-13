import asyncio
import httpx
import re
import json

async def scrape():
    url = 'https://maps.app.goo.gl/nCrAfYjEGqtY2bGC9'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        r = await client.get(url, headers=headers)
        print('Final URL:', str(r.url))
        print('Status:', r.status_code)
        print('HTML len:', len(r.text))

        # Check for title
        title_m = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE)
        if title_m:
            print('Title:', title_m.group(1))

        # Check for keywords from user's example
        for kw in ['Kaju Chicken', 'Mandi', 'Loose Motions', 'Currys', 'Devilking']:
            if kw.lower() in r.text.lower():
                print(f'Found keyword: {kw}')

        # Save HTML snippet to scratch for inspection
        with open('scratch_page.html', 'w', encoding='utf-8') as f:
            f.write(r.text)

if __name__ == '__main__':
    asyncio.run(scrape())
