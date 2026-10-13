import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def test_ask_search(restaurant_name, city="Hyderabad"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    query = f"{restaurant_name} {city} reviews"
    search_url = f"https://www.ask.com/web?q={urllib.parse.quote(query)}"
    
    print(f"Requesting Ask.com: {search_url}")
    
    try:
        r = requests.get(search_url, headers=headers, timeout=10.0)
        print("Status:", r.status_code)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Ask.com snippets are usually in <p class="PartialSearchResults-item-abstract"> or class containing abstract
        snippets = []
        for p in soup.find_all('p', class_='PartialSearchResults-item-abstract'):
            snippets.append(p.get_text().strip())
            
        if not snippets:
            # Fallback
            for p in soup.find_all('p'):
                txt = p.get_text().strip()
                if len(txt) > 35 and any(k in txt.lower() for k in ['food', 'mandi', 'taste', 'curry', 'money', 'poison', 'good', 'bad', 'place', 'order', 'restaurant', 'chicken', 'price', 'atmosphere', 'delicious']):
                    snippets.append(txt)
                    
        print("Snippets found:", len(snippets))
        for idx, s in enumerate(snippets[:10], 1):
            s_safe = s.encode('ascii', errors='replace').decode('ascii')
            print(f"  [{idx}] {s_safe}")
            
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    test_ask_search("BVS Mandi", "Hayathnagar Hyderabad")
