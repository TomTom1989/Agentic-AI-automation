from loaders import ItemLoader
from testing import Tester
from sklearn.svm import SVR
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import numpy as np

def get_bow_features(items):
    texts = [item.test_prompt() for item in items]
    prices = [item.price for item in items]
    vectorizer = CountVectorizer(max_features=1000, stop_words='english')
    X = vectorizer.fit_transform(texts)
    X_train, X_test, y_train, y_test = train_test_split(X, prices, test_size=0.1, random_state=42)
    return X_train, X_test, y_train, y_test, vectorizer

def train_svm_model(X_train, y_train):
    model = SVR(kernel='rbf', C=1.0, epsilon=0.2)  # You can tweak these hyperparameters
    model.fit(X_train, y_train)
    return model

def main():
    print("Loading items...")
    loader = ItemLoader("Appliances")
    items = loader.load()

    if len(items) < 10:
        print("Not enough items to train a model.")
        return

    print(f"{len(items)} items loaded.")

    # === Feature Extraction ===
    print("Extracting BoW features...")
    X_train, X_test, y_train, y_test, vectorizer = get_bow_features(items)

    # === Train Model ===
    print("Training SVR model...")
    model = train_svm_model(X_train, y_train)

    # === Predictor Function ===
    def predictor(item):
        X = vectorizer.transform([item.test_prompt()])
        prediction = model.predict(X)[0]
        return max(0.0, prediction)  # Ensure non-negative prices

    # === Evaluate ===
    print("Evaluating model...")
    tester = Tester(predictor, items, title="SVR (BoW)", size=len(items))
    tester.run()

if __name__ == "__main__":
    main()
