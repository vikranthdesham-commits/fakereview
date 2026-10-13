import urllib.request
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request('https://fakereviewcheck.com/', headers=headers)
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    print("HTML Length:", len(html))
    scripts = re.findall(r'src=["\']([^"\']+)["\']', html)
    print("Scripts:", scripts)
    
    # Check if there are JS files
    for s in scripts:
        if s.startswith('/') or s.startswith('http'):
            url = s if s.startswith('http') else 'https://fakereviewcheck.com' + s
            print("Fetching script:", url)
            s_req = urllib.request.Request(url, headers=headers)
            s_content = urllib.request.urlopen(s_req).read().decode('utf-8')
            print(f"Script {s} length: {len(s_content)}")
            # search for keywords
            matches = re.findall(r'.{0,50}(?:amazon|flipkart|score|trust|grade|ASIN|api|endpoint|POST|GET|json).{0,50}', s_content, re.IGNORECASE)
            print("Found matches in script:", len(matches))
            for m in matches[:15]:
                print("  -", m.strip())
except Exception as e:
    print("Error:", e)
