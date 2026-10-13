import requests
from bs4 import BeautifulSoup
import urllib.parse

def test_google_detailed(query):
    # Try with a clean mobile/desktop user agent
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&hl=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    
    r = requests.get(url, headers=headers, timeout=10.0)
    print("Google Status:", r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # In desktop Google search, search snippets are typically inside:
    # 1. Elements with attribute data-ved (descriptions)
    # 2. Divs with class "VwiC3b yD3zGc"
    # 3. Spans inside result blocks
    
    snippets = []
    # Method A: find divs with class VwiC3b (normal snippets)
    for div in soup.find_all('div', class_='VwiC3b'):
        snippets.append(div.get_text().strip())
        
    # Method B: find spans that contain review words
    if not snippets:
        for span in soup.find_all('span'):
            txt = span.get_text().strip()
            if len(txt) > 30 and any(k in txt.lower() for k in ['food', 'mandi', 'taste', 'service', 'curry', 'money', 'poison', 'good', 'bad', 'place', 'order', 'restaurant', 'chicken', 'price', 'atmosphere', 'delicious']):
                if not any(bad in txt.lower() for bad in ['settings', 'privacy', 'terms', 'google', 'maps', 'sign in']):
                    snippets.append(txt)
                    
    print(f"Google Extracted {len(snippets)} snippets:")
    for idx, s in enumerate(snippets[:10], 1):
        print(f"  [{idx}] {s}")

if __name__ == '__main__':
    test_google_detailed("B.Tech Bites Hayathnagar reviews")
