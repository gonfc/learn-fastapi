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
def root() -> dict[str, dict[int, Item]]:
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
        category: Category | None = None
) -> dict[str, Selection | list[Item]]:
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


@app.post('/')
def add_item(item: Item) -> dict[str, Item]:
    if item.id in items:
        raise HTTPException(status_code=400, detail=f'Item with {item.id=} is already exists the database.')
    items[item.id] = item
    return {"added": item}


@app.put('/items/{item_id}')
def update_item(
        # Requires an id
        item_id: int,
        name: str | None = None,
        price: float | None = None,
        count: int | None = None,
        category: Category | None = None
) -> dict[str, Selection | list[Item]]:
    if all(info is None for info in (name, price, count)):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update."
        )
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f'Item with {item_id=} does not found in the datbase.')
    item = items[item_id]
    if item.name is not None:
        item.name = name
    if item.price is not None:
        item.price = price
    if item.count is not None:
        item.count = count

    return dict['updated': item]


@app.delete('/items/{item_id}')
def delete_item_by_id(item_id: int) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(status_code=400, detail=f'Item with {item_id=} not detected in the database.')
    item = items[item_id]
    items.pop(item_id)
    return {f"deleted": item }
