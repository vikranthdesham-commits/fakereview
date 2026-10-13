import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def test_dynamic_follow():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    # Let's search BVS Mandi
    query = "BVS Mandi Hayathnagar Hyderabad reviews"
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&hl=en"
    
    print("Initial GET:", url)
    r = requests.get(url, headers=headers, timeout=10)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Try to find redirect link
    target_link = None
    for a in soup.find_all('a'):
        href = a.get('href') or ""
        if "/search?" in href:
            target_link = href
            break
            
    if not target_link:
        print("No redirect link found! Content might be direct search page or blocked.")
        # check if it's already the search page
        target_link = url
    else:
        # construct full url
        target_link = "https://www.google.com" + target_link
        print("Found redirect link! Following it:", target_link)
        r = requests.get(target_link, headers=headers, timeout=10)
        
    soup2 = BeautifulSoup(r.text, 'html.parser')
    
    # Let's save it to inspect
    with open('google_followed.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
        
    print("Followed page HTML length:", len(r.text))
    
    # In standard Google Search results, snippets are inside divs or spans:
    # 1. Search result snippets are typically in <div class="VwiC3b yD3zGc">
    # 2. Or inside blocks of reviews
    
    snippets = []
    
    # Check general text segments that look like reviews
    for div in soup2.find_all('div', class_=re.compile('VwiC3b|yD3zGc|MUjhb|BNeawe|s3oCkc')):
        txt = div.get_text().strip()
        snippets.append(txt)
        
    # If no snippets found by class, fetch any paragraph/span containing dining/food keywords
    if not snippets:
        for span in soup2.find_all(['span', 'div', 'p']):
            txt = span.get_text().strip()
            if len(txt) > 40 and any(k in txt.lower() for k in ['food', 'mandi', 'taste', 'curry', 'money', 'poison', 'good', 'bad', 'place', 'order', 'restaurant', 'chicken', 'price', 'atmosphere', 'delicious']):
                if not any(bad in txt.lower() for bad in ['settings', 'privacy', 'terms', 'google', 'maps', 'web search', 'sign in']):
                    snippets.append(txt)
                    
    print(f"Total snippets extracted: {len(snippets)}")
    for idx, s in enumerate(snippets[:10], 1):
        s_safe = s.encode('ascii', errors='replace').decode('ascii')
        print(f"  {idx}. {s_safe[:180]}")

if __name__ == '__main__':
    test_dynamic_follow()
