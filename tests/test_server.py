import os

import dotenv
import requests
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv('SERVER_URL')

assert requests.get(f"{SERVER_URL}").status_code == 200
assert requests.get(f"{SERVER_URL}/items/1").status_code == 200
