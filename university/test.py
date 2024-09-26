import requests

url = 'http://127.0.0.1:8000/departments'
response = requests.get(url)

print(response.status_code)
print(response.json())
