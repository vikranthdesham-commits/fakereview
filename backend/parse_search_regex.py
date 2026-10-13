import re

def parse_search():
    with open('google_search.html', 'r', encoding='utf-8') as f:
        html = f.read()

    print("HTML length:", len(html))
    
    # Extract text from tags using regex
    tags = re.findall(r'>([^<]{30,600})<', html)
    print(f"Total tag contents: {len(tags)}")

    keywords = ["mandi", "food", "taste", "service", "curry", "currys", "money", "poison", "good", "bad", "place", "order", "restaurant", "mutton", "chicken"]
    reviews = []
    for t in tags:
        clean = t.strip()
        clean_lower = clean.lower()
        if any(k in clean_lower for k in keywords):
            if not any(bad in clean_lower for bad in ["google", "javascript", "privacy", "terms", "sign in", "maps", "search", "http", "css"]):
                if clean not in reviews:
                    reviews.append(clean)

    print(f"\nExtracted {len(reviews)} real review text snippets:")
    for i, r in enumerate(reviews[:20], 1):
        print(f"\n[{i}] {r}")

if __name__ == '__main__':
    parse_search()
