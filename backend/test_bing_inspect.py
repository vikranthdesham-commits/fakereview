import requests
from bs4 import BeautifulSoup
import urllib.parse

def inspect_bing():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    query = "BVS Mandi Hayathnagar Hyderabad reviews"
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    
    r = requests.get(url, headers=headers, timeout=10.0)
    print("Bing Status:", r.status_code)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Let's save the HTML to inspect
    with open('bing_page.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
        
    print("HTML saved to bing_page.html. Length:", len(r.text))
    
    # In Bing search, result titles are typically inside <h2> and snippets inside <p> or <div class="b_caption"> or class "b_parastd"
    # Let's see all paragraphs
    p_tags = soup.find_all('p')
    print(f"Total <p> tags: {len(p_tags)}")
    for i, p in enumerate(p_tags[:10]):
        print(f"  P[{i}]: {p.get_text()[:120]}")
        
    # Let's see list items (Bing results are often inside <li class="b_algo">)
    algos = soup.find_all('li', class_='b_algo')
    print(f"Total <li class='b_algo'>: {len(algos)}")
    for i, li in enumerate(algos[:5]):
        print(f"  ALGO[{i}]: {li.get_text()[:200]}")

if __name__ == '__main__':
    inspect_bing()
