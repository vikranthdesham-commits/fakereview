import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def test_engines():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    query = "B.Tech Bites Hayathnagar reviews"
    
    # 1. Duckduckgo without slash
    url_ddg = f"https://html.duckduckgo.com/html?q={urllib.parse.quote(query)}"
    try:
        r = requests.get(url_ddg, headers=headers, timeout=10.0)
        print("DDG (no slash) status:", r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        snippets = soup.find_all('a', class_='result__snippet')
        print(f"  Snippets count: {len(snippets)}")
        if snippets:
            print("  Example:", snippets[0].get_text()[:100])
    except Exception as e:
        print("DDG Error:", e)
        
    # 2. Yahoo Search with desktop UA
    url_yahoo = f"https://search.yahoo.com/search?p={urllib.parse.quote(query)}"
    try:
        r = requests.get(url_yahoo, headers=headers, timeout=10.0)
        print("Yahoo status:", r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        snippets = []
        for d in soup.find_all('div', class_='compText'):
            snippets.append(d.get_text().strip())
        if not snippets:
            for p in soup.find_all('p'):
                txt = p.get_text().strip()
                if len(txt) > 30 and 'b.tech' in txt.lower():
                    snippets.append(txt)
        print(f"  Yahoo snippets count: {len(snippets)}")
        if snippets:
            print("  Example:", snippets[0][:100])
    except Exception as e:
        print("Yahoo Error:", e)

if __name__ == '__main__':
    test_engines()
