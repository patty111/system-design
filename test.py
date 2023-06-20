import requests
try:
    a = requests.get("https://example.com")
    print(a.status_code)
except:
    print("123")