from textblob import TextBlob
import json

def sentiment_analyzer(text: str) -> str:
    """
    Analyzes the sentiment and subjectivity of a text snippet (e.g., news or social post) 
    using TextBlob and derives a composite severity score for local issues.
    
    This tool is used by the Classifier Agent to quantify the emotional intensity 
    of a reported local issue, which is essential for the downstream Prioritizer Agent.
    
    Args:
        text (str): The raw text snippet to be analyzed. This text should ideally 
                    be focused on the core issue (e.g., a short headline or complaint).

    Returns:
        str: A JSON-formatted string containing the analysis results. The urgency 
             is mapped based on polarity. The 'severity_score' is the product of 
             polarity and subjectivity.
             
             Output structure:
             {
                 "issue_sentiment": "Positive" | "Negative" | "Neutral",
                 "issue_urgency": "High" | "Normal" | "Low",
                 "severity_score": float,  # (Polarity * Subjectivity) range approx [-1.0 to 1.0]
                 "raw_subjectivity": float # The raw TextBlob subjectivity score [0.0 to 1.0]
             }
    """
    textBlob = TextBlob(text)
    text_polarity = textBlob.sentiment.polarity
    text_subjectivity = textBlob.sentiment.subjectivity
    sentiment, urgency = '', ''
    
    if text_polarity > 0.1:
        sentiment = "Positive"
        urgency = "Low"
    elif text_polarity < -0.1:
        sentiment = "Negative"
        urgency = "High"
    else:
        sentiment = "Neutral"
        urgency = "Normal"
    
    severity_score = text_subjectivity * text_polarity     
    result = {
        "issue_sentiment": sentiment,
        "issue_urgency": urgency,
        "severity_score": severity_score, 
        "raw_subjectivity": text_subjectivity
    }
    
    return json.dumps(result)