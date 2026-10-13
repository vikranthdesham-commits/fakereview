import requests
from bs4 import BeautifulSoup
import urllib.parse

def check():
    query = "BVS Mandi reviews"
    url = f"https://www.mojeek.com/search?q={urllib.parse.quote(query)}"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # print all tag names and counts
    counts = {}
    for el in soup.find_all(True):
        counts[el.name] = counts.get(el.name, 0) + 1
    print("Tags found:", counts)
    
    body = soup.find('body')
    if body:
        txt = " ".join(body.get_text().split())
        safe_txt = txt.encode('ascii', errors='replace').decode('ascii')
        print("Mojeek content:")
        print(safe_txt[:1000])

if __name__ == '__main__':
    check()
