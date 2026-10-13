import re

FOOD_KEYWORDS = {
    "biryani", "mandi", "pizza", "pizzas", "burger", "burgers", "fries", "pasta", "dosa", "dosas",
    "idli", "idlis", "vada", "vadas", "roti", "rotis", "naan", "naans", "curry", "curries", "kabab",
    "kababs", "kebab", "kebabs", "shawarma", "shawarmas", "soup", "soups", "salad", "salads",
    "sandwich", "sandwiches", "wrap", "wraps", "samosa", "samosas", "manchurian", "noodles",
    "tenders", "tikka", "tikkas", "masala", "masalas", "paneer", "chicken", "mutton", "fish",
    "prawn", "prawns", "rice", "gravy", "gravies", "dal", "chutney", "chutneys", "sambhar", "cake",
    "cakes", "brownie", "brownies", "tiramisu", "dessert", "desserts", "ice cream", "ice-cream",
    "chai", "tea", "coffee", "shake", "shakes", "garlic bread", "salan", "meetha", "halwa"
}

STOP_AND_SENTIMENT_WORDS = {
    # Stop words/conjunctions/pronouns
    "the", "a", "an", "our", "their", "here", "there", "in", "at", "on", "to", "this", "that",
    "these", "those", "some", "we", "i", "you", "they", "he", "she", "it", "my", "your", "his",
    "her", "have", "has", "had", "was", "is", "were", "are", "very", "so", "extremely", "really",
    "quite", "too", "also", "just", "ordered", "got", "eating", "served", "dined", "cooked",
    "prepare", "prepared", "tried", "bought", "takeaway", "about", "with", "and", "or", "but",
    "for", "of", "as", "then", "order", "orders", "place", "places", "one", "some", "any", "all",
    "out", "thru", "through", "main", "road", "shop", "going", "money", "waste", "time", "day", "night",
    # Emotive/Subjective Adjectives
    "delicious", "tasty", "good", "bad", "worst", "amazing", "great", "excellent", "outstanding",
    "phenomenal", "exceptional", "perfect", "horrible", "terrible", "dry", "cold", "hot", "warm",
    "fresh", "authentic", "famous", "rich", "sweet", "mild", "spicy", "heavy", "soft", "hard",
    "nice", "proper", "special", "unprofessional", "soggy", "watered", "rubbery", "tough", "stale",
    "disappointed", "lukewarm", "expensive", "cheap", "overpriced", "clean", "dirty", "unhygienic",
    "rude", "polite",
    # Non-food nouns commonly found near food names
    "wrong", "delivered", "toppings", "topping", "side", "portion", "portions", "size", "sizes", 
    "taste", "tasted", "quality", "experience", "price", "prices", "value", "food", "items", "item", 
    "dine", "dining", "menu", "outlet", "outlets", "customer", "customers", "staff", "waiter", 
    "waiters", "service", "management", "test"
}

def extract_best_and_worst_items(restaurant_name: str, reviews: list) -> tuple:
    # Only look at genuine reviews to score items (suspicion_score < 45)
    genuine_reviews = [r for r in reviews if r.get("suspicion_score", 0) < 45.0]
    target_reviews = genuine_reviews if genuine_reviews else reviews
    if not target_reviews:
        return None, None

    scores = {}

    pos_words = ["delicious", "good", "perfect", "amazing", "phenomenal", "outstanding", "exceptional", "loved", "tasty", "fresh", "best", "great", "rich", "favorite", "flavorful", "clean", "polite", "juicy"]
    neg_words = ["worst", "rubbery", "cold", "tough", "stale", "bad", "disappointed", "horrible", "terrible", "watered", "oily", "hard", "lukewarm", "expensive", "soggy", "unprofessional", "rude", "watered down"]

    for rev in target_reviews:
        text = rev["text"].lower()
        rating = rev.get("rating", 3)

        # Split sentence into phrases by basic sentence endings
        sentences = re.split(r'[.!?\n\r]+', text)
        for sentence in sentences:
            # Split sentences dynamically by conjunctions & punctuation to isolate dish name clauses
            parts = re.split(r'[,;:\-\(\)]|\band\b|\bor\b|\bwith\b|\bbut\b|\bfor\b|\bof\b|\bas\b|\bthen\b|\bby\b', sentence)
            for part in parts:
                words = [w.strip(" .,?!();:\"'’“”-") for w in part.split()]
                words = [w for w in words if w]
                
                # Check for food keywords and extract contiguous segments around them
                for i, w in enumerate(words):
                    if w in FOOD_KEYWORDS:
                        # Extract contiguous words before and after that are not stop words (max 2 words each side)
                        start_idx = i
                        while start_idx > max(0, i - 2) and words[start_idx - 1] not in STOP_AND_SENTIMENT_WORDS:
                            start_idx -= 1
                            
                        end_idx = i
                        while end_idx < min(len(words) - 1, i + 2) and words[end_idx + 1] not in STOP_AND_SENTIMENT_WORDS:
                            end_idx += 1
                        
                        dish_words = words[start_idx:end_idx + 1]
                        # Join and cleanse
                        dish = " ".join(dish_words).strip(" .,?!();:\"'’“”-").title()
                        
                        # Only keep if dish name is meaningful (not empty and has more than just stop words)
                        if dish and dish.lower() not in STOP_AND_SENTIMENT_WORDS:
                            if dish not in scores:
                                scores[dish] = 0.0
                            
                            # Score base rating
                            if rating >= 4:
                                scores[dish] += 2.0
                            elif rating <= 2:
                                scores[dish] -= 2.0
                                
                            # Check nearby words inside the sentence for sentiment
                            for p in pos_words:
                                if p in sentence:
                                    scores[dish] += 1.0
                            for n in neg_words:
                                if n in sentence:
                                    scores[dish] -= 1.0

    # Filter out items with 0 score
    non_zero_scores = {k: v for k, v in scores.items() if v != 0}
    
    best_item = None
    worst_item = None

    if non_zero_scores:
        # Find best item (must be positive score)
        best_cand = max(non_zero_scores, key=non_zero_scores.get)
        if non_zero_scores[best_cand] > 0:
            best_item = best_cand
            
        # Find worst item (must be negative score)
        worst_cand = min(non_zero_scores, key=non_zero_scores.get)
        if non_zero_scores[worst_cand] < 0:
            worst_item = worst_cand

    # Resolve edge case conflict
    if best_item and worst_item and best_item == worst_item:
        if scores[best_item] > 0:
            worst_item = None
        else:
            best_item = None

    return best_item, worst_item

# Test cases
mock_bvs_mandi = [
    {"text": "The Currys here are SO delicious. We ordered the Kaju Chicken and Butter chicken mild and the flavour was exceptional. The portions are really big. The curry was so delicious we even ordered one takeaway for dinner tonight. I highly recommend this place.", "rating": 5, "suspicion_score": 5},
    {"text": "Good service nd best prices teast was suppr", "rating": 5, "suspicion_score": 5},
    {"text": "It seems to be acquired by a new management now. I had ordered a takeaway of Mutton Juicy Mandi. Most places give you Mutton and rice cooked together. Here, you are provided with some dry rice with an accompaniment of mutton pieces.", "rating": 3, "suspicion_score": 5},
    {"text": "Please don't waste your Money by going to this Restaurant. I had chicken Mandi and got Loose Motions and Food Poison and Heavy stomach ache and Gas Problem, Heart Burn. This is a Genuine Review 🙏🏻🙏🏻...", "rating": 1, "suspicion_score": 5},
    {"text": "Located on main road. Shop is open. Just clicked the pic while passing thru Highway. Looks good from out.", "rating": 4, "suspicion_score": 5},
    {"text": "(mandi)The food was good until it was hot .... It felt a little expensive for the food quality So soup when we came to eat .. but the service was good and people were polite", "rating": 3, "suspicion_score": 5},
    {"text": "Mutton mandi test was delicious 😍 and all over items are good and testy 🤤🤤", "rating": 5, "suspicion_score": 5},
    {"text": "Taste Is Good But Prices Are Much High 🥲", "rating": 3, "suspicion_score": 5}
]

# Alternate reviews for Karsh Mandi (originally identical, now changed to check uniqueness)
mock_karsh_mandi = [
    {"text": "Tried their Faham Mandi, chicken was cooked perfectly, very juicy. Seating arrangement is nice.", "rating": 5, "suspicion_score": 10},
    {"text": "Outstanding Creamy Garlic Mayo and Seekh Kababs. Highly recommend to everyone in the area.", "rating": 5, "suspicion_score": 10},
    {"text": "The Grilled Chicken Shawarma was very rubbery and cold. Highly disappointed.", "rating": 2, "suspicion_score": 10},
    {"text": "Nice mandi rice taste, but service is slow.", "rating": 3, "suspicion_score": 10}
]

mock_dominos = [
    {"text": "The Cheese Burst pizza was extremely fresh and hot! Garlic bread dipping sauce was delicious. Prompt delivery within 30 minutes.", "rating": 5, "suspicion_score": 5},
    {"text": "Great service at this Domino's branch. Order was prepared cleanly and Choco Lava Cake was warm and rich.", "rating": 5, "suspicion_score": 5},
    {"text": "BEST PIZZA EVER 100% PERFECT MUST BUY DOMINOS DISCOUNT PROMO CODE TODAY!", "rating": 5, "suspicion_score": 90}, # suspicious
    {"text": "Pizza base was slightly over-baked and dry. Service counter was busy during weekend peak hours.", "rating": 3, "suspicion_score": 5},
    {"text": "Wrong pizza toppings delivered and cold side orders. Customer support was slow to assist.", "rating": 1, "suspicion_score": 5}
]

mock_paradise = [
    {"text": "World famous Mutton Dum Biryani! The basmati rice grains were long, fragrant, and perfectly spiced. Mirchi ka salan was spot on.", "rating": 5, "suspicion_score": 5},
    {"text": "Chicken 65 and Double ka Meetha were outstanding. Polite waiting staff and quick service despite heavy afternoon rush.", "rating": 5, "suspicion_score": 5},
    {"text": "BEST BIRYANI IN HYDERABAD 100/100 PERFECT MUST VISIT DISCOUNTS CODE NOW!", "rating": 5, "suspicion_score": 85}, # suspicious
    {"text": "Biryani quality is good, but finding car parking during peak hours is very tough.", "rating": 4, "suspicion_score": 5},
    {"text": "Biryani was lukewarm and chicken pieces were tough. Expected much better quality from Paradise.", "rating": 2, "suspicion_score": 5}
]

print("BVS Mandi:")
print(extract_best_and_worst_items("BVS Mandi", mock_bvs_mandi))

print("\nKarsh Mandi (Diversified):")
print(extract_best_and_worst_items("Karsh Mandi", mock_karsh_mandi))

print("\nDomino's Pizza:")
print(extract_best_and_worst_items("Domino's Pizza", mock_dominos))

print("\nParadise Biryani:")
print(extract_best_and_worst_items("Paradise Biryani", mock_paradise))
