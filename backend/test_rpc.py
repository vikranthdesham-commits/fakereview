import asyncio
import httpx
import re
import urllib.parse

async def test_rpc():
    # Test 1: Google Maps place preview RPC endpoint
    place_name = "BVS Mandi Restaurant"
    encoded_name = urllib.parse.quote(place_name)
    url = f"https://www.google.com/maps/preview/place?q={encoded_name}&pb=!1m14!1m12!1m3!1d1000!2d78.688!3d17.309!2m3!1f0!2f0!3f0!3m2!1i1000!2i1000!4f13.1!7i20!10b1!12m6!2m3!5m1!6e2!20e3!10b1!16b1!19m4!2m3!1i360!2i120!4i8!20m57!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80!2m2!1i80!2i80"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        r = await client.get(url, headers=headers)
        print('RPC Status:', r.status_code)
        print('RPC Content Length:', len(r.text))

        # Check for keywords from user's example in the RPC response!
        for kw in ['Kaju Chicken', 'Mandi', 'Loose Motions', 'Devilking', 'Srikanth', 'ANSAL', 'Cecil', 'Sritesh', 'Vankudoth']:
            if kw.lower() in r.text.lower():
                print(f'-> FOUND MATCH FOR USER REVIEW KEYWORD: {kw}')

        with open('rpc_response.txt', 'w', encoding='utf-8') as f:
            f.write(r.text)

if __name__ == '__main__':
    asyncio.run(test_rpc())
