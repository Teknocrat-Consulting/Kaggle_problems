from transformers import pipeline

spam_classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")

# Example messages
messages = [
    "Congratulations! You've won a $1000 Walmart gift card. Go to http://bit.ly/123456 to claim now.",
    "Hi there, are we still meeting for coffee tomorrow?",
    "URGENT! Your account has been compromised. Please click on the link to secure your account.",
    
]

# Classify each message
results = spam_classifier(messages)

# Interpret labels
label_map = {
    "LABEL_1": "spam",
    "LABEL_0": "ham"
}

# Print the results
for message, result in zip(messages, results):
    label = label_map[result['label']]
    print(f"Message: {message}\nPrediction: {label} (Score: {result['score']:.4f})\n")
