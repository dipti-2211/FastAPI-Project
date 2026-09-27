from fastapi import FastAPI, HTTPException
from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return {"message": "hi This is demo work"}


products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1000,
        "in_stock": True
    },
    {
        "id": 2,
        "name": "Mouse",
        "price": 200,
        "in_stock": True
    },
    {
        "id": 3,
        "name": "Keyboard",
        "price": 300,
        "in_stock": True
    },
    {
        "id": 4,
        "name": "Key",
        "price": 30,
        "in_stock": True
    },
    {
        "id": 5,
        "name": "charger",
        "price": 0,
        "in_stock": False
    }
]


@app.get("/products")
def get_products():
    return products

@app.get("/id/{id}")
def get_products_id(id: int):
    for prod in products:
        if prod["id"] == id :
            return prod 

    return "product not found !!"