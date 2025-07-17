from loaders import ItemLoader
from testing import Tester
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

def get_bow_features(items):
    texts = [item.test_prompt() for item in items]
    prices = [item.price for item in items]
    vectorizer = CountVectorizer(max_features=1000, stop_words='english')
    X = vectorizer.fit_transform(texts)
    X_train, X_test, y_train, y_test = train_test_split(X, prices, test_size=0.1, random_state=42)
    return X_train, X_test, y_train, y_test, vectorizer

def train_linear_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def main():
    # === Load data ===
    print("Loading items...")
    loader = ItemLoader("Appliances")
    items = loader.load()

    if len(items) < 10:
        print("Not enough items to train a model.")
        return

    print(f"{len(items)} items loaded.")

    # === Feature extraction (BoW) ===
    print("Extracting BoW features...")
    X_train, X_test, y_train, y_test, vectorizer = get_bow_features(items)

    # === Train linear regression model ===
    print("Training Linear Regression model...")
    model = train_linear_model(X_train, y_train)

    # === Define a predictor function ===
    def predictor(item):
        X = vectorizer.transform([item.test_prompt()])
        return model.predict(X)[0]

    # === Evaluate ===
    print("Evaluating model...")
    tester = Tester(predictor, items, title="Linear Regression", size=len(items))

    tester.run()


if __name__ == "__main__":
    main()
