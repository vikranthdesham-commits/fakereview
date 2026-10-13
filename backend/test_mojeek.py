import requests
from bs4 import BeautifulSoup
import urllib.parse

def test_mojeek():
    query = "BVS Mandi Hayathnagar Hyderabad reviews"
    url = f"https://www.mojeek.com/search?q={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("Requesting Mojeek:", url)
    try:
        r = requests.get(url, headers=headers, timeout=10.0)
        print("Status:", r.status_code)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # snippets on Mojeek are typically under class "s" or inside paragraphs of the result list
        snippets = []
        for s in soup.find_all('p', class_='s'):
            snippets.append(s.get_text().strip())
            
        print("Snippets found:", len(snippets))
        for idx, s in enumerate(snippets[:10], 1):
            s_safe = s.encode('ascii', errors='replace').decode('ascii')
            print(f"  [{idx}] {s_safe}")
            
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    test_mojeek()
