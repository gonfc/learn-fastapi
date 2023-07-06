import os

import dotenv
import requests
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv('SERVER_URL')

assert requests.get(f"{SERVER_URL}").status_code == 200
assert requests.get(f"{SERVER_URL}/items/1").status_code == 200

assert requests.get(f"{SERVER_URL}/items?name=plier").json().get(['selection'][0]) == [{'name': 'plier', 'price': 6.99, 'count': 70, 'id': 1, 'category': 'tools'}]
assert requests.get(f"{SERVER_URL}/items?price=6.99").json().get(['selection'][0]) != ''
assert requests.get(f"{SERVER_URL}/items?category=tools").json() != ''

assert requests.post(url=SERVER_URL, json={"name": 'pvc_hinge', "price": 1.99, "count": 50, "id": 4, "category": "tools"}).status_code == 200
assert requests.delete(url=SERVER_URL + '/items/4', json={"item_id": 4}).status_code == 200
# TODO
# assert 'pvc_hinge' not in requests.get(url=SERVER_URL).json()