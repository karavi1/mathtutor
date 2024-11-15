from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from src.backend.crud.query import get_resources
from src.backend.categorization.categorize import get_categories

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None



## Sample Methods to check if app is working
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


## Core Functionality
@app.get("/maths/{topic}")
def get_resources_by_topic(topic: str):
    ## TODO: Add image processing gate to categorization, fetch topic response and feed to CRUD query to database
    resource = get_resources([topic])
    return {"topic": topic, "resource": resource}


@app.get("/demo/{problem}")
def get_resources_for_problem(problem: str):
    categories = get_categories(problem)
    resources = get_resources(categories)
    response = {
        "problem": problem,
        "categories": categories,
        "resources": resources
    }
    return response
