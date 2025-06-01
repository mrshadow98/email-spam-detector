import joblib
import base64
import quopri
import re

model = joblib.load('data/spam_classifier_model.joblib')

def preprocess_gmail_message(raw_email):
    """
    Extracts and cleans up the plain text content of a Gmail message
    from the 'raw_email' structure as returned by the Gmail API.
    """

    # Step 1: Extract the base64 encoded body from part with "text/plain"
    parts = raw_email.get("payload", {}).get("parts", [])
    text_part = next((part for part in parts if part.get("mimeType") == "text/plain"), None)
    if not text_part:
        return None

    encoded_body = text_part.get("body", {}).get("data", "")
    if not encoded_body:
        return None

    # Step 2: Gmail encodes with URL-safe base64 (replace - and _)
    decoded_bytes = base64.urlsafe_b64decode(encoded_body + '===')

    # Step 3: Decode quoted-printable content
    quoted_printable_decoded = quopri.decodestring(decoded_bytes)

    # Step 4: Convert bytes to UTF-8 string and clean up noise characters
    decoded_text = quoted_printable_decoded.decode("utf-8", errors="ignore")

    # Step 5: Remove excessive unicode noise like '\u034f', '\u200c', etc.
    cleaned_text = re.sub(r'[\u034f\u200c\u200b\u200d]+', '', decoded_text)

    # Step 6: Strip extra whitespace
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text


def predict_spam(email):
    email = preprocess_gmail_message(email)
    return "Spam" if model.predict([email])[0] == 1 else "Not Spam"