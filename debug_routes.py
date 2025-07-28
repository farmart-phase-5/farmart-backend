import requests

BASE_URL = "http://127.0.0.1:5000"

routes_to_test = [
    # (METHOD, ENDPOINT, SAMPLE_DATA)
    ("GET", "/animals", None),
    ("GET", "/animals/1", None),
    ("POST", "/animals", {"name": "Cow", "breed": "Zebu", "age": 3, "farmer_id": 1}),
    
    ("GET", "/farmers/1/animals", None),
    ("GET", "/farmers/", None),
    ("POST", "/farmers/register", {"name": "Joel", "location": "Nairobi"}),

    ("GET", "/orders", None),
    ("GET", "/orders/1", None),
    ("GET", "/orders/users/1/orders", None),
    ("POST", "/orders", {"user_id": 1, "total_amount": 2500}),
    
    ("GET", "/orders/1/items", None),
    ("GET", "/orders/items?animal_id=456", None),

    ("GET", "/cart_items?page=1&per_page=10", None),
    ("POST", "/cart_items", {"cart_id": 1, "animal_id": 1, "quantity": 2}),
    
    ("GET", "/carts/1", None),
    ("POST", "/carts", {"user_id": 1}),
]

def test_route(method, endpoint, data=None):
    full_url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(full_url)
        elif method == "POST":
            response = requests.post(full_url, json=data)
        elif method == "PATCH":
            response = requests.patch(full_url, json=data)
        else:
            print(f"Unsupported method {method} for {endpoint}")
            return

        print(f"[{method}] {endpoint} ➜ Status: {response.status_code}")
        if response.status_code not in [200, 201]:
            print(f"    ⚠️ Response: {response.text}")

    except Exception as e:
        print(f"[{method}] {endpoint} ➜ ERROR: {e}")

if __name__ == "__main__":
    print("📡 Debugging Flask Routes...\n")
    for method, endpoint, data in routes_to_test:
        test_route(method, endpoint, data)
