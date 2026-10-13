from bs4 import BeautifulSoup

with open('google_followed.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
print("Title of followed page:", soup.find('title'))
body = soup.find('body')
if body:
    txt = " ".join(body.get_text().split())
    safe_txt = txt.encode('ascii', errors='replace').decode('ascii')
    print("Body content (first 1000 chars):")
    print(safe_txt[:1000])
