import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

### 📄 Load CSV
df = pd.read_csv("data/spam_assassin.csv")  # update with your actual path

# Drop any rows with missing text
df.dropna(subset=['text'], inplace=True)

X = df['text']
y = df['target']

### 🔀 Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

### 🏗 Build Model Pipeline
model = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=3000,
        stop_words='english',
        lowercase=True
    )),
    ('clf', LogisticRegression(max_iter=1000))
])

### 🚂 Train
model.fit(X_train, y_train)

### 📊 Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

### 💾 Save model for reuse
joblib.dump(model, 'data/spam_classifier_model.joblib')
print("✅ Model saved as spam_classifier_model.joblib")
