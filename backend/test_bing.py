import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def test_bing_search(restaurant_name, city=""):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    query = f"{restaurant_name} {city} reviews"
    search_url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    
    print(f"Query URL: {search_url}")
    
    try:
        r = requests.get(search_url, headers=headers, timeout=10.0)
        print("Status:", r.status_code)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Bing search snippets are typically inside <p> or <div class="b_caption"> or class "b_parastd"
        snippets = []
        for p in soup.find_all(['p', 'span']):
            txt = p.get_text().strip()
            if len(txt) > 35 and any(k in txt.lower() for k in ['food', 'mandi', 'taste', 'service', 'curry', 'money', 'poison', 'good', 'bad', 'place', 'order', 'restaurant', 'chicken', 'price', 'atmosphere', 'delicious']):
                if not any(bad in txt.lower() for bad in ['bing', 'microsoft', 'privacy', 'terms', 'sign in', 'settings', 'cookies', 'wikipedia']):
                    if txt not in snippets:
                        snippets.append(txt)
                        
        print("Snippets found:", len(snippets))
        for idx, s in enumerate(snippets[:10], 1):
            print(f"[{idx}] {s}")
            
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    test_bing_search("B.Tech Bites", "Hayathnagar")
