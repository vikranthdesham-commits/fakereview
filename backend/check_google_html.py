from bs4 import BeautifulSoup

try:
    with open('google_search.html', 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    print("Title of Google Search page:", soup.find('title'))
    print("Sample content:")
    txt = " ".join(soup.get_text().split())
    safe_txt = txt.encode('ascii', errors='replace').decode('ascii')
    print(safe_txt[:800])
except Exception as e:
    print("Error:", e)
