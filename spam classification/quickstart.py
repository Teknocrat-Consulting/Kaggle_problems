import requests

url = 'http://localhost:5000/predict'
data = {'email': 'Congratulations! You''ve won a $1000 Walmart gift card. Go to http://bit.ly/123456 to claim now'}

"""
1 = spam
0 = not spam
"""
response = requests.post(url, json=data)
print(response.json())
