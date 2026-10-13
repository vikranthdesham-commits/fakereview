import httpx
import re
from urllib.parse import unquote

url = 'https://maps.app.goo.gl/NfdYhRm56QGzbUAg6'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

with httpx.Client(follow_redirects=True, headers=headers, timeout=15.0) as client:
    resp = client.get(url)
    final_url = str(resp.url)
    print("Final URL:", final_url)
    
    # 1. Improved regex for /maps/place/
    match = re.search(r'/maps/place/([^/@?]+)', final_url)
    if match:
        raw_segment = unquote(match.group(1)).replace('+', ' ').strip()
        # Remove any trailing slash or data
        place_name = raw_segment.split('/')[0].strip()
        print("Clean Place Name:", place_name)

    # 2. Extract q= parameter if available
    q_match = re.search(r'[?&]q=([^&]+)', final_url)
    if q_match:
        q_val = unquote(q_match.group(1)).replace('+', ' ').strip()
        print("Q Param:", q_val)

    # 3. Check for meta description / og tags or schema JSON-LD in HTML
    schema_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', resp.text, re.DOTALL)
    print("Found JSON-LD scripts:", len(schema_matches))
    for s in schema_matches:
        print("JSON-LD:", s[:300])

    # Check for text in html
    title_matches = re.findall(r'og:title.*?content="([^"]+)"', resp.text)
    print("OG Titles:", title_matches)

    # Check for meta description
    desc_matches = re.findall(r'meta.*?name="Description".*?content="([^"]+)"', resp.text)
    print("Descriptions:", desc_matches)
