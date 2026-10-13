from bs4 import BeautifulSoup
import re

with open('google_search.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
meta = soup.find('meta', attrs={'http-equiv': re.compile('refresh', re.IGNORECASE)})
if meta:
    print("Meta refresh found:", meta)
    content = meta.get('content')
    print("Content:", content)
else:
    print("No meta refresh")

# Check all links
links = soup.find_all('a')
print("Total links:", len(links))
for idx, a in enumerate(links):
    print(f"  Link {idx}: text={a.get_text()} href={a.get('href')}")
