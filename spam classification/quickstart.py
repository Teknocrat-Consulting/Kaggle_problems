import requests

url = 'http://localhost:5000/predict'
data = {'email': 'Hi where you. You in home or calicut?,,,'}

"""
1 = spam
0 = not spam
"""
response = requests.post(url, json=data)
print(response.json())
