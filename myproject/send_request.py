import requests

URL = 'http://localhost:3000'

try:
    response = requests.get(f'{URL}/add-and-get/')
    print(response.text)
except Exception as e:
    print(e)