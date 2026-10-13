import asyncio
from scratch_real_web_scraper import get_real_live_google_reviews

async def test():
    revs, name, addr = await get_real_live_google_reviews("https://maps.app.goo.gl/nCrAfYjEGqtY2bGC9")
    print("=== BVS MANDI SCRAPED REVIEWS ===")
    print("Name:", name)
    print("Address:", addr)
    print(f"Total Extracted: {len(revs)}")
    for i, r in enumerate(revs, 1):
        print(f"[{i}] ({r['rating']} stars): {r['text'][:140]}")

    print("\n" + "="*50 + "\n")

    revs2, name2, addr2 = await get_real_live_google_reviews("Dominos Pizza Hayathnagar")
    print("=== DOMINOS PIZZA SCRAPED REVIEWS ===")
    print("Name:", name2)
    print("Address:", addr2)
    print(f"Total Extracted: {len(revs2)}")
    for i, r in enumerate(revs2, 1):
        print(f"[{i}] ({r['rating']} stars): {r['text'][:140]}")

if __name__ == '__main__':
    asyncio.run(test())
