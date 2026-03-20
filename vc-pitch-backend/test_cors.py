import urllib.request
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/examples",
    method="GET",
    headers={
        "Origin": "http://127.0.0.1:5500"
    }
)
try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.status}")
        print(f"Headers: {response.getheaders()}")
        print(f"Text: {response.read().decode('utf-8')[:50]}")
except urllib.error.HTTPError as e:
    print(f"Error Status: {e.code}")
    print(f"Error Headers: {e.headers}")
    print(f"Error Text: {e.read().decode('utf-8')[:50]}")
