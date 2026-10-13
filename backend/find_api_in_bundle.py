import urllib.request
import re

url = 'https://fakereviewcheck.com/assets/index-oX4c_-x_.js'
headers = {'User-Agent': 'Mozilla/5.0'}
content = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read().decode('utf-8')

# Search for fetch calls or endpoints
endpoints = re.findall(r'fetch\([^\)]+\)|axios\.[a-z]+\([^\)]+\)|https?://[a-zA-Z0-9\.\-\_/]+', content)
print("Found calls/URLs:", len(endpoints))
for ep in list(set(endpoints))[:30]:
    if 'google' not in ep and 'cloudflare' not in ep and 'w3.org' not in ep:
        print("  *", ep)
