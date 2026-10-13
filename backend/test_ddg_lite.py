import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def test_ddg_lite(restaurant_name, address=""):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    query = f"{restaurant_name} {address} reviews"
    search_url = f"https://lite.duckduckgo.com/lite/?q={urllib.parse.quote(query)}"
    
    print(f"Query Lite URL: {search_url}")
    
    try:
        r = requests.get(search_url, headers=headers, timeout=10.0)
        print("Status:", r.status_code)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # DuckDuckGo Lite snippets are typically inside <td> containing result snippet text, or class "result-snippet"
        # Let's inspect class or dump table content
        snippets = []
        
        # In DDG Lite, results are structured in a table. The snippets are usually in a row with class "result-snippet"
        # or inside td elements with class "result-snippet" or elements following the result title.
        for td in soup.find_all('td', class_='result-snippet'):
            snippets.append(td.get_text().strip())
            
        if not snippets:
            # Fallback to general parsing if class names differ
            for row in soup.find_all('tr'):
                text = row.get_text().strip()
                if "reviews" in text.lower() or "rating" in text.lower():
                    # clean up spacing
                    clean_text = " ".join(text.split())
                    if len(clean_text) > 40 and not any(bad in clean_text.lower() for bad in ['settings', 'privacy', 'terms']):
                        snippets.append(clean_text)
                        
        print("Snippets found:", len(snippets))
        for idx, s in enumerate(snippets[:10], 1):
            print(f"[{idx}] {s[:150]}")
            
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    test_ddg_lite("BVS Mandi", "Hayathnagar Hyderabad")
