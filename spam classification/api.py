from flask import Flask, request, jsonify
import pickle
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import string

ps = PorterStemmer()

cv = pickle.load(open("model/vectorizer.pkl", "rb"))
clf = pickle.load(open("model/model1.pkl", "rb"))

app = Flask(__name__)


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        userInput = data['email']
        print("Received input:", userInput)
        
        # Transform input text
        userInput = transform_text(userInput)
        print("Transformed input:", userInput)
        
        # Vectorize input
        result = cv.transform([userInput]).toarray()
        print("Vectorized input shape:", result.shape)
        
        # Make prediction
        pred = clf.predict(result)[0]
        print("Prediction:", pred)
        
        return jsonify({'prediction': int(pred)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
if __name__ == "__main__":
    app.run(debug=True)
