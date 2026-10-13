import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def test_yahoo_search(restaurant_name, address=""):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    city = "Hyderabad" if "hyderabad" in address.lower() else ""
    query = f"{restaurant_name} {city} reviews"
    search_url = f"https://search.yahoo.com/search?p={urllib.parse.quote(query)}"
    
    print(f"Query URL: {search_url}")
    
    try:
        r = requests.get(search_url, headers=headers, timeout=10.0)
        print("Status:", r.status_code)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Yahoo snippets style: divs with class "compText aBc" etc., or <p class="lh-16">
        # Let's search all paragraphs or divs that look like paragraphs/descriptions
        snippets = []
        for p in soup.find_all(['p', 'span']):
            txt = p.get_text().strip()
            if len(txt) > 35 and any(k in txt.lower() for k in ['food', 'mandi', 'taste', 'service', 'curry', 'money', 'poison', 'good', 'bad', 'place', 'order', 'restaurant', 'chicken', 'price', 'atmosphere', 'delicious']):
                if not any(bad in txt.lower() for bad in ['yahoo', 'search', 'terms', 'privacy', 'sign in', 'settings', 'cookies']):
                    if txt not in snippets:
                        snippets.append(txt)
                        
        print("Snippets found:", len(snippets))
        for idx, s in enumerate(snippets[:10], 1):
            print(f"[{idx}] {s}")
            
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    test_yahoo_search("B.Tech Bites", "Hayathnagar Hyderabad")
