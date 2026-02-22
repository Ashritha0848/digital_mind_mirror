from textblob import TextBlob

def analyze_text(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    if sentiment > 0.2:
        mood = "Positive"
    elif sentiment < -0.2:
        mood = "Negative"
    else:
        mood = "Neutral"

    confidence_keywords = ["confident", "strong", "achieve", "win", "success"]
    stress_keywords = ["stress", "tired", "anxious", "pressure", "fear"]

    words = text.lower().split()

    confidence_score = sum(word in confidence_keywords for word in words)
    stress_score = sum(word in stress_keywords for word in words)

    return {
        "sentiment": sentiment,
        "mood": mood,
        "confidence_score": confidence_score,
        "stress_score": stress_score
    }