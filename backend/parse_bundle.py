import urllib.request
import re

url = 'https://fakereviewcheck.com/assets/index-oX4c_-x_.js'
headers = {'User-Agent': 'Mozilla/5.0'}
content = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read().decode('utf-8')

# Search for strings in the React bundle
strings = re.findall(r'["\']([^"\'\n]{10,120})["\']', content)
clean_strings = [s for s in strings if any(k in s.lower() for k in ['amazon', 'flipkart', 'review', 'trust', 'rating', 'grade', 'score', 'url', 'fake', 'flag', 'burst', 'analys', 'adjusted', 'http'])]
print(f'Total matched strings: {len(clean_strings)}')
for s in list(set(clean_strings))[:50]:
    print(' -', s)
