import asyncio
import httpx
import re
import json
from urllib.parse import unquote

async def fetch_gmaps_rpc_reviews(google_maps_url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    # Step 1: Resolve final URL to get the Place Hex ID / Feature ID (e.g. 0x3bcb0b2f0dd1fa27:0x1e3dcc974a5e7b9c)
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        r = await client.get(google_maps_url, headers=headers)
        final_url = str(r.url)
        html = r.text

    print("Final URL:", final_url)

    # Extract feature ID (1s0x...:0x...)
    feature_match = re.search(r'1s(0x[0-9a-f]+:0x[0-9a-f]+)', final_url, re.IGNORECASE)
    if not feature_match:
        # Search HTML for feature ID
        feature_match = re.search(r'(0x[0-9a-f]{16}:0x[0-9a-f]{16})', html, re.IGNORECASE)

    feature_id = feature_match.group(1) if feature_match else None
    print("Feature ID found:", feature_id)

    if feature_id:
        # Google Maps RPC listugcposts endpoint for live reviews
        rpc_url = f"https://www.google.com/maps/rpc/listugcposts?authuser=0&hl=en&gl=us&pb=!1m7!1s{feature_id}!3m1!1s{feature_id}!6m10!1m2!1s1!2zZW4!2m1!1s1!3m1!1s1!5m1!1s1!2m2!1i10!2i1!3m1!1s1!5m2!1s1!2zZW4!"
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            rpc_resp = await client.get(rpc_url, headers=headers)
            print("RPC Response Status:", rpc_resp.status_code)
            print("RPC Response Len:", len(rpc_resp.text))
            
            with open("rpc_reviews.txt", "w", encoding="utf-8") as f:
                f.write(rpc_resp.text)

            # Extract review strings from RPC response (RPC returns JS array format `)]}'\n[...`)
            # Text strings are embedded as JSON elements inside the nested arrays
            text_snippets = re.findall(r'\"([A-Z0-9][^\"]{20,1000}?[\.!\?])\"', rpc_resp.text)
            print(f"Extracted {len(text_snippets)} review text snippets from Google Maps RPC!")
            for i, txt in enumerate(text_snippets[:10], 1):
                print(f"[{i}] {txt}")

if __name__ == '__main__':
    asyncio.run(fetch_gmaps_rpc_reviews("https://maps.app.goo.gl/nCrAfYjEGqtY2bGC9"))
