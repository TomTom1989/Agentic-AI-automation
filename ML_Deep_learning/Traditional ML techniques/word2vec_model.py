from loaders import ItemLoader
from testing import Tester
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import gensim.downloader as api

# === Load pre-trained GloVe model (100d, auto-downloaded) ===
print("Loading GloVe Word2Vec model (this may take a few seconds)...")
word_vectors = api.load("glove-wiki-gigaword-100")
print("GloVe model loaded.")

def get_avg_word2vec_features(items):
    texts = [item.test_prompt() for item in items]
    prices = [item.price for item in items]
    features = []

    for text in texts:
        words = text.split()
        vecs = [word_vectors[word] for word in words if word in word_vectors]
        if vecs:
            features.append(np.mean(vecs, axis=0))
        else:
            features.append(np.zeros(word_vectors.vector_size))

    X = np.array(features)
    y = np.array(prices)

    return train_test_split(X, y, test_size=0.1, random_state=42)

def train_linear_model(X_train, y_train):
    model = LinearRegression()
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
    print("Extracting Word2Vec features...")
    X_train, X_test, y_train, y_test = get_avg_word2vec_features(items)

    # === Model Training ===
    print("Training Linear Regression model...")
    model = train_linear_model(X_train, y_train)

    # === Predictor Function ===
    def predictor(item):
        words = item.test_prompt().split()
        vecs = [word_vectors[word] for word in words if word in word_vectors]
        if vecs:
            vec = np.mean(vecs, axis=0).reshape(1, -1)
        else:
            vec = np.zeros((1, word_vectors.vector_size))
        prediction = model.predict(vec)[0]
        return max(0.0, prediction)  # Clamp negative predictions to zero


    # === Evaluation ===
    print("Evaluating model...")
    tester = Tester(predictor, items, title="Linear Regression (GloVe Word2Vec)", size=len(items))
    tester.run()

if __name__ == "__main__":
    main()
