import requests, certifi

print(certifi.where)
print(certifi.where())

urls = "https://google.com"

response = requests.get(urls)

print(response)
