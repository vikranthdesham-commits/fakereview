import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def test_requests_ddg(restaurant_name, address=""):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    city = "Hyderabad" if "hyderabad" in address.lower() else ""
    query = f"{restaurant_name} {city} reviews"
    search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    
    print(f"Query URL: {search_url}")
    
    try:
        r = requests.get(search_url, headers=headers, timeout=10.0)
        print("Status:", r.status_code)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        snippets = soup.find_all('a', class_='result__snippet')
        print("Snippets found:", len(snippets))
        
        reviews = []
        for s in snippets:
            txt = s.get_text().strip()
            txt_clean = re.sub(r'^\d+\s*reviews?\s*·?\s*', '', txt, flags=re.IGNORECASE).strip()
            reviews.append(txt_clean)
        
        print("\nFiltered snippets:")
        for idx, rev in enumerate(reviews[:10], 1):
            print(f"[{idx}] {rev}")
            
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    test_requests_ddg("B.Tech Bites", "Hyderabad")
