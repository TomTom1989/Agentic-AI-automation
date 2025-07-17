from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

def get_bow_features(items, max_features=1000):
    texts = [item.test_prompt() for item in items]
    prices = [item.price for item in items]

    vectorizer = CountVectorizer(max_features=max_features, stop_words="english")
    X = vectorizer.fit_transform(texts)
    y = prices

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, vectorizer
