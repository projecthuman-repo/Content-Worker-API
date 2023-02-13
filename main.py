from typing import Union

from fastapi import FastAPI

app = FastAPI()

# Base route returning an object of hello world
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Route to manage queries within the request URL
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}