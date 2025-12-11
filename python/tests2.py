import requests

URL = "http://localhost:5000"

r = requests.post(f"{URL}/users", json={"name": "Dd", "email": "D@d"})

try:
    print(r.json())
except Exception:
    print(r.text())

r = requests.get(f"{URL}/users")

print(r.json())

r = requests.get(f"{URL}/users", params={"name":"Dd"})

print(r.json())