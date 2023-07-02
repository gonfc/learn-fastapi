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
def get_items_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} was not found in the database.")
    return items[item_id]


Selection = dict[str, str | int | float | Category | None]


@app.get('/items/')
def get_items_by_parameters(
        name: str | None = None,
        price: float | None = None,
        count: int | None = None,
        category: Category | None = None) \
        -> dict[str, Selection | list[Item]]:
    def check_item_validity(item: Item):
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count != count,
                category is None or item.category is category
            )
        )

    selection = [item for item in items.values() if check_item_validity(item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection
    }