import joblib

model = joblib.load('data/spam_classifier_model.joblib')

def predict_spam(email):
    return "Spam" if model.predict([email])[0] == 1 else "Not Spam"