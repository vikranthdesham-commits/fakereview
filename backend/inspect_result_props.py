import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://fakereviewcheck.com/assets/index-oX4c_-x_.js'
headers = {'User-Agent': 'Mozilla/5.0'}
content = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read().decode('utf-8')

for key in ['trust_score', 'adjusted_rating', 'red_flags', 'grade', 'verdict', 'product_title', 'store', 'rating_distribution', 'review_breakdown']:
    idx = content.find(key)
    if idx != -1:
        print(f"=== Found '{key}' at index {idx} ===")
        print(content[max(0, idx - 200):min(len(content), idx + 800)])
        print("\n" + "="*50 + "\n")
