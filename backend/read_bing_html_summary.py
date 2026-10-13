from bs4 import BeautifulSoup

with open('bing_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
print("Title:", soup.find('title'))

body = soup.find('body')
if body:
    print("\nBody text sample:")
    txt = " ".join(body.get_text().split())
    safe_txt = txt.encode('ascii', errors='replace').decode('ascii')
    print(safe_txt[:1200])
else:
    print("\nNo body found.")
