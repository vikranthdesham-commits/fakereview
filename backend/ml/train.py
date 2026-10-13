import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Sample training dataset combining e-commerce & restaurant reviews (Ott et al. + Kaggle style)
TRAIN_DATA = [
    # Genuine reviews
    ("The battery life is decent, lasts about a day with moderate use. Build quality feels sturdy.", 0),
    ("Food was good, especially the wood-fired pizza. Service was a bit slow during weekend rush hour.", 0),
    ("Installed easily on my kitchen tap. No leaks so far. Packaging was plain but safe.", 0),
    ("Decent pair of running shoes for the price. Sizing runs slightly tight around the toes.", 0),
    ("Nice ambiance, cozy seating. The pasta was cooked al dente, but tomato sauce needed more garlic.", 0),
    ("Works as expected. Screen brightness is great outdoors. Camera is average in low light.", 0),
    ("Ordered chicken biryani. Portions were generous, spice level was authentic. Will revisit.", 0),
    ("Fabric is soft 100% cotton, comfortable for summer wear. Stitches are neat.", 0),
    ("Sound quality is warm and balanced. Earcups get slightly warm after 2 hours.", 0),
    ("Staff was polite and greeted us. Coffee was freshly brewed and hot.", 0),
    ("Item arrived 2 days late, box had a small dent, but product inside was intact and works fine.", 0),
    ("Tastes good, not too sweet. Good natural ingredient list.", 0),
    ("Good build quality for the price. Buttons have tactile feedback.", 0),
    ("Portion size was fair. Clean restrooms and quick billing.", 0),

    # Suspicious / Fake reviews
    ("AMAZING PRODUCT BEST EVER BUY NOW WOW FIVE STARS HIGHLY RECOMMENDED MUST HAVE!!!", 1),
    ("This restaurant is the absolute pinnacle of culinary mastery! Unbelievable food, world class staff, 1000 stars!", 1),
    ("EXCELLENT SUPERB QUALITY AMAZING SERVICE BEST IN THE WORLD PERFECT PERFECT PERFECT!", 1),
    ("DO NOT BUY TOTAL SCAM TRASH DISASTER BROKE IN ONE SECOND REGRET EVERYTHING!", 1),
    ("Literally the greatest product ever invented in human history! Changed my life completely, buy 10 items right now!", 1),
    ("Outstanding incredible magnificent fantastic spectacular superior quality 10/10!", 1),
    ("Pure perfection! The owner is an angel, food was blessed by gods, never eaten anything better anywhere on earth!", 1),
    ("Fast shipping fast delivery top seller best quality buy buy buy!", 1),
    ("HORRIBLE WORST PLACE EVER EVER EVER DISGUSTING FOUL SCAMMER FAKE UNBELIEVABLE BAD!", 1),
    ("Best quality best price best service best experience! Must order today without delay!", 1),
    ("Mindblowing miraculous perfection! 10 stars isn't enough, absolutely flawlessly phenomenal!", 1),
    ("Extremely good product highly recommend to everyone in the universe!", 1),
    ("Life changing experience! Words cannot describe how insanely great this item is!", 1),
    ("BEST OF THE BEST OF THE BEST! ALWAYS BUY FROM THIS BRAND ONLY!", 1)
]

def train_and_save():
    artifacts_dir = os.path.join(os.path.dirname(__file__), "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)

    texts, labels = zip(*TRAIN_DATA)
    
    vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1, 2), stop_words='english')
    X = vectorizer.fit_transform(texts)
    
    model = LogisticRegression(C=1.0)
    model.fit(X, labels)

    preds = model.predict(X)
    acc = accuracy_score(labels, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')

    print(f"Training Complete! Accuracy: {acc:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}")

    joblib.dump(vectorizer, os.path.join(artifacts_dir, "vectorizer.joblib"))
    joblib.dump(model, os.path.join(artifacts_dir, "model.joblib"))
    print("Model & Vectorizer saved to ml/artifacts/")

if __name__ == "__main__":
    train_and_save()
