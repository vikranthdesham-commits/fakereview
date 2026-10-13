import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

html = urllib.request.urlopen(urllib.request.Request('https://fakereviewcheck.com/', headers=headers)).read().decode('utf-8')
print("HTML content:")
print(html)
