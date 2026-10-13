import urllib.request
import re

url = 'https://fakereviewcheck.com/assets/index-oX4c_-x_.js'
headers = {'User-Agent': 'Mozilla/5.0'}
content = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read().decode('utf-8')

idx = content.find('/analyze')
if idx != -1:
    start = max(0, idx - 1000)
    end = min(len(content), idx + 2000)
    print("Code surrounding /analyze:")
    print(content[start:end])
