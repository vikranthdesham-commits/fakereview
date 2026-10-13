import asyncio
import httpx
import re

async def test_ddg():
    query = 'site:google.com/maps/place "BVS Mandi Restaurant"'
    url = 'https://html.duckduckgo.com/html/'
    data = {'q': query}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        r = await client.post(url, data=data, headers=headers)
        print('DDG Status:', r.status_code)
        
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', r.text, re.DOTALL)
        print(f"DDG Snippets found: {len(snippets)}")
        for s in snippets:
            clean = re.sub(r'<[^>]+>', '', s).strip()
            print("Snippet:", clean)

if __name__ == '__main__':
    asyncio.run(test_ddg())
