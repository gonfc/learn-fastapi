from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Set

app = FastAPI()

from dotenv import load_dotenv

load_dotenv()


class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"


class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category


items = {
    0: Item(name='hammer', price=19.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name='plier', price=6.99, count=70, id=1, category=Category.TOOLS),
    2: Item(name='monster', price=1.99, count=500, id=2, category=Category.CONSUMABLES)
}


@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}


@app.get('/items/{item_id}')
def index(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} was not found in the database.")
    return items[item_id]
