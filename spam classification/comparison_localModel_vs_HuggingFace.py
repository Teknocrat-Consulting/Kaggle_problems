import requests
import csv
from transformers import pipeline

import pandas as pd


local_url = 'http://localhost:5000/predict'

# Hugging Face BERT-based model for spam detection
spam_classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")

df = pd.read_csv('spam.csv', encoding='ISO-8859-1')
df['v1']
messages = (df['v2'][1:500])
original_val = list(df['v1'][1:500])

results = []


for message,org in zip(messages,original_val):
    data = {'email': message}
    response = requests.post(local_url, json=data)
    local_result = response.json()
    print(local_result)
    local_prediction = "spam" if local_result['prediction'] == 1 else "ham"
    
  
    hf_results = spam_classifier(message)
    hf_prediction = "spam" if hf_results[0]['label'] == "LABEL_1" else "ham"
    results.append({'Message': message, 'Local_Prediction': local_prediction, 'HF_Prediction': hf_prediction ,'orginal_val':org })

# Writing results to a CSV file
with open('spam_detection_results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Message', 'Local_Prediction', 'HF_Prediction','orginal_val']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        writer.writerow(result)
