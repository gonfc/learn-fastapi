import os

import dotenv
import requests
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv('SERVER_URL')

assert requests.get(f"{SERVER_URL}").status_code == 200
assert requests.get(f"{SERVER_URL}/items/1").status_code == 200

assert requests.get("http://127.0.0.1:8000/items?name=plier").json().get(['selection'][0]) == [{'name': 'plier', 'price': 6.99, 'count': 70, 'id': 1, 'category': 'tools'}]
assert requests.get("http://127.0.0.1:8000/items?price=6.99").json().get(['selection'][0]) != ''
assert requests.get("http://127.0.0.1:8000/items?category=tools").json() != ''
